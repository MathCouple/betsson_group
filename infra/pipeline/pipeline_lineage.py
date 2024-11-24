"""
This module will hold specific functions to handle
full lineage stages for the pipeline.
"""
from datetime import datetime
from typing import Callable

import pandas as pd

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
    def __init__(self, bg_logger, f_sanitize_text: Callable):
        """
        Initialize the PipelineTransformer.

        Args:
            f_sanitize_text: A callable function to normalize string columns.
            bg_logger: Logger instance for logging.
        """
        self.bg_logger = bg_logger
        self.f_sanitize_text = f_sanitize_text

    def stage_1(self, f_sanitize_column_data: Callable, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the first stage of transformations to the data.
        Args:
            df: DataFrame containing the data.
        Returns:
            The transformed DataFrame.
        """
        start_time = datetime.now()

        # Specialized string dtypes
        df['Invoice'] = f_sanitize_column_data(
            self.bg_logger, df, 'Invoice', 
        )
        df['StockCode'] = f_sanitize_column_data(
            self.bg_logger, df, 'StockCode', 
        )
        df['Description'] = f_sanitize_column_data(
            self.bg_logger, df, 'Description', 
        )
        df['Customer ID'] = f_sanitize_column_data(
            self.bg_logger, df, 'Customer ID', 
        )
        df['Country'] = f_sanitize_column_data(
            self.bg_logger, df, 'Country', 
        )

        # Specialized numeric dtypes, NaN for invalid values
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        # Specialized datetime to ISO 8601, NaT for invalid values
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        # Sanitize well-known column names
        df.columns = ['invoice', 'stock_code', 'description', 'quantity', 'invoice_date', 'price', 'customer_id', 'country']

        self.bg_logger.info(
            "Stage 1 transformations completed in %s", 
            str(datetime.now() - start_time)
        )
        return df

    def save_parquet_stage(self, df: pd.DataFrame, file_path: str, **kwargs):
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
