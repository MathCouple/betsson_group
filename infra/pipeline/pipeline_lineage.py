"""
This module will hold specific functions to handle
full lineage stages for the pipeline.
"""
import re
from datetime import datetime
from typing import Callable

import pandas as pd

from infra.pipeline import (
    NORMATIZE_LOCATION_MAP,
    CLOUD_LOST_PRODUCTS_WORDS,
    STAGE_III_COLUMNS,
    generate_warehouse_sales_tables,
    validate_warehouse_sales_data,
    validation_models,
    validate_data_integrity
)
from infra.models.dim import (
    DimTime,
    DimLocation,
    DimCustomer,
    DimProduct,
    DimMetadataTransaction
)
from infra.models.fact import (
    FactSalesTransaction
)



escaped_keywords = [re.escape(word) for word in CLOUD_LOST_PRODUCTS_WORDS if word]


def get_csv_df(bg_logger, file_path, **kwargs) -> pd.DataFrame:
    """
    Reads a CSV file into a DataFrame.
    Args:
        bg_logger: Logger instance for logging.
        file_path: Path to the CSV file.
    Returns:
        The DataFrame.
    """
    start_time = datetime.now()
    df = pd.read_csv(
        file_path,
        **kwargs
    )
    bg_logger.info("CSV file read into DataFrame in %s", str(datetime.now() - start_time))
    return df


class PipelineTransformer:
    """
    A class responsible for applying transformation logic for different stages of the pipeline.
    """
    def __init__(self, bg_logger, f_sanitize_text: Callable, f_sanitize_column_data: Callable):
        """
        Initialize the PipelineTransformer.

        Args:
            f_sanitize_text: A callable function to normalize string columns.
            bg_logger: Logger instance for logging.
        """
        self.bg_logger = bg_logger
        self.f_sanitize_text = f_sanitize_text
        self.f_sanitize_column_data = f_sanitize_column_data

    def stage_1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the first stage of transformations to the data.
        Args:
            df: DataFrame containing the data.
        Returns:
            The transformed DataFrame.
        """
        start_time = datetime.now()

        # Specialized string dtypes
        df['Country'] = df['Country'].apply(self.f_sanitize_text)
        # correct acronyms and normalizing location names
        df['Country'] = df['Country'].replace(NORMATIZE_LOCATION_MAP)
        self.bg_logger.info("Stage I Country Column transformed")

        # flag entry errors
        df['entry_errors'] = (
            df['Description'].isnull() &
            df['Customer ID'].isnull() &
            (df['Price'] <= 0)
        ).astype(int)
        self.bg_logger.info("Stage I Customer ID column transformed")

        # filter negative and zero prices as well as possible effective sales
        _non_and_zero_prices_df = df.query("Price <= 0")
        _possile_effective_sales = df.query("Price > 0")

        # seek for possible product returns
        _possible_product_returns = _non_and_zero_prices_df.merge(
            _possile_effective_sales,
            on=['Invoice', 'StockCode'],
            suffixes=('_return', '_sale')
        )

        _possile_effective_sales = None
        _non_and_zero_prices_df = None

        # filter out possible product returns
        _possible_product_returns = _possible_product_returns.query(
            "Quantity_return < Quantity_sale"
        )

        # flag product returns
        df['product_return'] = df.apply(
            lambda x: 1 if x['Invoice']
            in _possible_product_returns.loc[:, 'Invoice'].values else 0,
            axis=1
        )

        _possible_product_returns = None

        # Flag cloud lost products based on the pattern
        # Create the regex pattern to match only at the start of the string
        _pattern = r'^(?:' + '|'.join(escaped_keywords) + r')\b'
        df['lost_sales'] = df['Description'].str.contains(
            _pattern,
            case=False,
            na=False
        ).astype(int)
        _pattern = None
        self.bg_logger.info("Stage I Price column transformed")

        _pattern = 'debt|credit| fee'
        _fin_details_df = df[df['Description'].str.contains(_pattern, na=False, case=False)]

        # flag financial details
        df.loc[
            (df['Invoice'].isin(_fin_details_df['Invoice'])) &
            (df['StockCode'].isin(_fin_details_df['StockCode'])),
            'financial_details'
        ] = 1

        # flag adjustment and maintenance
        _pattern = 'adjust|update'
        df.loc[
            df['Description'].str.contains(_pattern, na=False, case=False),
            'maintenance_adjustment'
        ] = 1
        _pattern = None

        self.bg_logger.info("Stage I Description column transformed")

        # filter out gift products and bank charges
        _gift_df = df[
            df['StockCode'].astype(str).str.contains(
                'gift', na=False, regex=True, case=False
            )
        ]
        _charges_df = df[
            df['StockCode'].astype(str).str.contains(
                'charges', na=False, regex=True, case=False
            )
        ]

        # flag possible returns
        _return_sales_df = df[
            df['Quantity'] < 0
        ]
        df.loc[
            df['Invoice'].isin(_return_sales_df['Invoice']),
            'product_return'
        ] = 1
        _return_sales_df = None

        # flagging lost sales for gift products
        df.loc[
            (df['Invoice'].isin(_gift_df['Invoice'])) &
            (df['StockCode'].isin(_gift_df['StockCode'])),
            'lost_sales'
        ] = 1
        _gift_df = None

        # flagging bank charges as financial details
        df.loc[
            (df['Invoice'].isin(_charges_df['Invoice'])) &
            (df['StockCode'].isin(_charges_df['StockCode'])),
            'financial_details'
        ] = 1
        _charges_df = None
        self.bg_logger.info("Stage I StockCode column transformed")

        self.bg_logger.info("Stage I completed in %s", str(datetime.now() - start_time))
        return df

    def stage_2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the second stage of transformations to the data.
        Args:
            df: DataFrame containing the data.
        Returns:
            The transformed DataFrame.
        """
        start_time = datetime.now()

        # filtering test data
        _pattern = 'test|tste|tst'
        _test_data = df[
            df.astype(str)
            .apply(lambda col: col.str.contains(_pattern, case=False, regex=True))
            .any(axis=1)
        ]
        _pattern = None

        # updating entry errors
        df.loc[
            (df['Invoice'].isin(_test_data['Invoice'])) &
            (df['StockCode'].isin(_test_data['StockCode'])),
            'entry_errors'
        ] = 1
        _test_data = None

        self.bg_logger.info("Stage II General columns updated")

        self.bg_logger.info("Stage II completed in %s", str(datetime.now() - start_time))
        return df

    def stage_3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the third stage of transformations to the data.
        Args:
            df: DataFrame containing the data.
        Returns:
            The transformed DataFrame.
        """
        start_time = datetime.now()

        # removing entry errors
        df = df[~df['entry_errors'].astype(bool)]
        # removing entry errors column
        df.drop(columns=['entry_errors'], inplace=True)
        self.bg_logger.info("Stage III Entry errors filtered out")

        # correcting column names
        df.columns = STAGE_III_COLUMNS
        df.rename(columns={'country': 'location'}, inplace=True)
        self.bg_logger.info("Stage III Column names corrected")

        # formating dtypes on data
        df['invoice'] = self.f_sanitize_column_data(self.bg_logger, df, 'invoice')
        df['stock_code'] = self.f_sanitize_column_data(self.bg_logger, df, 'stock_code')
        df['description'] = self.f_sanitize_column_data(self.bg_logger, df, 'description')
        df['customer_id'] = self.f_sanitize_column_data(self.bg_logger, df, 'customer_id')
        df['location'] = self.f_sanitize_column_data(self.bg_logger, df, 'location')

        # specialized DTYPES
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # treating different date formats and converting to ISO 8601
        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df['invoice_date'] = df['invoice_date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        self.bg_logger.info("Stage III Data formatted")

        df.drop_duplicates(inplace=True)
        self.bg_logger.info("Stage III Duplicates removed")

        self.bg_logger.info("Stage III completed in %s", str(datetime.now() - start_time))
        return df

    def generates_dw_tables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the fourth stage of transformations to the data.
        Args:
            df: DataFrame containing the data.
        Returns:
            The transformed DataFrame.
        """
        start_time = datetime.now()
        # generates dw tables
        _tables = generate_warehouse_sales_tables(self.bg_logger, df)
        _generating_integrity_test = (
            validate_warehouse_sales_data(self.bg_logger, _tables, validation_models)
        )

        validate_data_integrity(self.bg_logger, _generating_integrity_test)
        self.bg_logger.info(
            "Stage IV Data Warehouse tables generated in %s",
            str(datetime.now() - start_time)
        )

    def save_parquet_stage(
        self, df: pd.DataFrame,
        file_path: str,
        **kwargs
    ):
        """
        Saves a DataFrame to a Parquet file.
        Args:
            df: DataFrame to be saved.
            file_path: Path to save the Parquet file.
            kwargs: Additional arguments for saving the Parquet file.
        """
        start_time = datetime.now()
        df.to_parquet(file_path, **kwargs)
        self.bg_logger.info(
            "DataFrame saved to Parquet in %s", 
            str(datetime.now() - start_time)
        )
