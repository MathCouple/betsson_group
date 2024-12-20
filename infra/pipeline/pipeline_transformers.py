"""
Module specialized on data transformation functions.
"""
import warnings
from hashlib import md5
from typing import (
    Dict,
    Any,
    Type
)
import re
import unicodedata
from datetime import datetime

from pydantic import ValidationError
from pydantic import BaseModel
import pandas as pd


warnings.filterwarnings("ignore")


def generate_hash(value: str) -> str:
    """
    Generates a consistent hash for a given string value.
    Handles None values gracefully.
    """
    if value is None or pd.isna(value):
        return None
    return md5(str(value).encode()).hexdigest()

def sanitize_column_data(bg_logger, df, column, c_dtype=str):
    """
    Corrects and specializes the data column format, replacing invalid values with NaN.
    Args:
        bg_logger: Logger instance for logging.
        df: DataFrame containing the data.
        column: Column to be transformed.
        c_dtype: Target data type (default is str).
    Returns:
        The transformed column.
    """
    start_time = datetime.now()
    df[column] = df[column].str.strip()

    bg_logger.info(
        "Specializing column data '%s' to '%s'. It took %s",
        column, str(c_dtype), str(datetime.now() - start_time)
    )
    return df[column]

def sanitize_text(text):
    """
    Normalizes text by:
    - Removing special characters
    - Replacing accented characters with their unaccented counterparts
        Note: This is a symbol-based scenario, meaning it only considers simple transformations.
        For words requiring special handling (e.g., unique characters in specific languages),
        we would need to either create a custom mapping or use a specialized
        library for broader support.
    - Removing extra spaces

    Args:
        text (str): The input string to normalize.

    Returns:
        str: The normalized text.
    """
    if not isinstance(text, str):
        return text  # Return as-is if not a string

    # 1. Remove accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

    # 2. Remove special characters*
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # 3. Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

class BaseTableGenerator:
    """
    Base class for table generation with shared preprocessing methods.
    """
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def standardize_category(self, row: Dict[str, any]) -> str:
        """
        Maps specific columns to standardized categories.
        """
        if row.get("product_return") == 1:
            return "return"
        if not pd.isna(row.get("financial_details")):
            return "financial adjustment"
        if not pd.isna(row.get("maintenance_adjustment")):
            return "maintenance adjustment"
        if row.get("lost_sales") == 1:
            return "lost sale"
        return "sale"

    def preprocess(self):
        """
        Standardize and prepare data for all tables.
        """
        self.df['transaction_category'] = self.df.apply(self.standardize_category, axis=1)

        # Parse invoice_date and extract time components
        self.df['invoice_date'] = pd.to_datetime(self.df['invoice_date'], errors='coerce')
        self.df['year'] = self.df['invoice_date'].dt.year
        self.df['quarter'] = self.df['invoice_date'].dt.quarter
        self.df['month'] = self.df['invoice_date'].dt.month
        self.df['day'] = self.df['invoice_date'].dt.day
        self.df['week'] = self.df['invoice_date'].dt.isocalendar().week
        self.df['day_of_week'] = self.df['invoice_date'].dt.day_name()
        self.df['price'] = self.df['price'].fillna(0.0)

        self.df['time_id'] = self.df['invoice_date'].apply(
            lambda x: generate_hash(str(pd.Timestamp(x).timestamp()))
        )
        # Generate IDs directly in the main DataFrame
        # preserving null references
        self.df['location_id'] = self.df['location'].apply(
            lambda x: generate_hash(str(x))
        )
        self.df['product_id'] = self.df['stock_code'].apply(
            lambda x: generate_hash(str(x))
        )
        self.df['metadata_id'] = self.df['transaction_category'].apply(
            lambda x: generate_hash(str(x))
        )
        self.df['customer_code'] = self.df['customer_id']
        self.df['customer_id'] = self.df['customer_code'].apply(
            lambda x: generate_hash(str(x))
        )

        self.df['transaction_id'] = self.df.apply(
            lambda row: generate_hash(f"{row['invoice']}-{row['time_id']}"), axis=1
        )

class DimTimeGenerator(BaseTableGenerator):
    """
    Generates the dim_time table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_time table from the preprocessed data.
        """
        dim_time = self.df[[
            'time_id', 'year', 'quarter',
            'month', 'day', 'week', 'day_of_week'
        ]].drop_duplicates(subset=['time_id'])
        dim_time.dropna(subset=['time_id'], inplace=True)
        return dim_time

class DimLocationGenerator(BaseTableGenerator):
    """
    Generates the dim_location table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_location table from the preprocessed data.
        """
        dim_location = self.df[[
            'location_id', 'location'
        ]].drop_duplicates(subset=['location_id'])
        dim_location.rename(columns={'location': 'location_name'}, inplace=True)
        return dim_location

class DimProductGenerator(BaseTableGenerator):
    """
    Generates the dim_product table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_product table from the preprocessed data.
        """
        dim_product = self.df[
            ['product_id', 'stock_code', 'description']
        ].drop_duplicates(subset=['product_id'])
        return dim_product

class DimMetadataTransactionGenerator(BaseTableGenerator):
    """
    Generates the dim_metadata_transactions table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_metadata_transactions table from the preprocessed data.
        """
        dim_metadata_transactions = self.df[[
            'metadata_id', 'transaction_category'
        ]].drop_duplicates(subset=['metadata_id'])
        dim_metadata_transactions['transaction_description'] = (
            dim_metadata_transactions['transaction_category'].str.title()
        )
        return dim_metadata_transactions

class DimCustomerGenerator(BaseTableGenerator):
    """
    Generates the dim_customer table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_customer table from the preprocessed data.
        """
        dim_customer = self.df[
            ['customer_id', 'customer_code']
        ].drop_duplicates(subset=['customer_id'])
        dim_customer['is_known_customer'] = dim_customer['customer_code'].notna()
        return dim_customer

class FactSalesTransactionGenerator(BaseTableGenerator):
    """
    Generates the fact_sales_transactions table.
    """
    def generate_table(self) -> pd.DataFrame:
        """ 
        Creates the fact_sales_transactions table from the preprocessed data.
        """
        # filtering columns
        fact_sales_transactions = self.df[[
            'transaction_id', 'time_id', 'location_id',
            'customer_id', 'product_id',
            'metadata_id', 'invoice',
            'quantity', 'price'
        ]].copy()
        fact_sales_transactions.rename(columns={'invoice': 'invoice_id'}, inplace=True)
        return fact_sales_transactions

def generate_warehouse_sales_tables(bg_logger, data: pd.DataFrame):
    """
    Generates all tables required for the warehouse_sales database.

    Args:
        bg_logger: Logger instance for logging.
        data (pd.DataFrame): The input data to generate tables from.
    
    Returns:
        Dict[str, pd.DataFrame]: A dictionary mapping table names to their corresponding DataFrames.
    """
    base_gen = BaseTableGenerator(data)
    base_gen.preprocess()
    bg_logger.info("Data preprocessed successfully.")

    dim_time_gen = DimTimeGenerator(base_gen.df)
    dim_time = dim_time_gen.generate_table()
    bg_logger.info("dim_time table generated successfully.")

    dim_location_gen = DimLocationGenerator(base_gen.df)
    dim_location = dim_location_gen.generate_table()
    bg_logger.info("dim_location table generated successfully.")

    dim_product_gen = DimProductGenerator(base_gen.df)
    dim_product = dim_product_gen.generate_table()
    bg_logger.info("dim_product table generated successfully.")

    dim_metadata_gen = DimMetadataTransactionGenerator(base_gen.df)
    dim_metadata_transactions = dim_metadata_gen.generate_table()
    bg_logger.info("dim_metadata_transactions table generated successfully.")

    dim_customer_gen = DimCustomerGenerator(base_gen.df)
    dim_customer = dim_customer_gen.generate_table()
    bg_logger.info("dim_customer table generated successfully.")

    fact_gen = FactSalesTransactionGenerator(base_gen.df)
    fact_sales_transactions = fact_gen.generate_table()
    bg_logger.info(
        "fact_sales_transactions table generated successfully."
    )

    bg_logger.info("All tables generated successfully.")
    return {
        'dim_time': dim_time,
        'dim_location': dim_location,
        'dim_product': dim_product,
        'dim_customer': dim_customer,
        'dim_metadata_transactions': dim_metadata_transactions,
        'fact_sales_transactions': fact_sales_transactions,
    }

def validate_warehouse_sales_data(
    bg_logger,
    dataframes: Dict[str, pd.DataFrame],
    validation_models: Dict[str, Type[BaseModel]],
    return_valid_rows: bool = False
) -> Dict[str, Any]:
    """
    Validates the data in each table against its corresponding Pydantic model.

    Args:
        bg_logger:
            Logger for logging validation information.
        dataframes (Dict[str, pd.DataFrame]): A dictionary mapping table names to Pandas DataFrames.
        validation_models (Dict[str,
            Type[BaseModel]]): A dictionary mapping table names to Pydantic validation models.
        return_valid_rows (bool): If True, includes valid rows in the results.

    Returns:
        Dict[str, Any]: Validation results, including errors and optionally valid rows if any exist.
    """
    bg_logger.info("Validating data...")

    results = {}
    for table_name, df in dataframes.items():
        bg_logger.info(f"Validating table: {table_name}")
        model = validation_models.get(table_name)
        if not model:
            raise ValueError(f"No validation model found for table: {table_name}")

        errors = []
        valid_rows = []

        for idx, row in df.iterrows():
            try:
                # pylint: disable=unused-variable
                # Attempt to validate the row
                validated_row = model(**row.to_dict())
                if return_valid_rows:
                    valid_rows.append(row)
            except ValidationError as e:
                # Collect validation errors
                errors.append({"row_index": idx, "error": e.errors()})

        results[table_name] = {
            "valid_rows_count": len(df) - len(errors),
            "invalid_rows_count": len(errors),
            "errors": errors,
            "valid_rows": pd.DataFrame(valid_rows) if return_valid_rows else None,
        }

    return results

def validate_data_integrity(bg_logger, data_integrity_check: Dict[str, Any]):
    """
    Logs the results of the data integrity check.
    """

    for table, result in data_integrity_check.items():
        bg_logger.info(f"Table: {table}")
        bg_logger.info(f"Valid rows: {result.get('valid_rows_count', 0)}")
        bg_logger.info(f"Invalid rows: {result.get('invalid_rows_count', 0)}")

        if result.get("errors"):
            bg_logger.info(f"Errors: {result['errors'][:2]}")

        bg_logger.info("*" * 32)
    bg_logger.info("Data integrity check completed.")
