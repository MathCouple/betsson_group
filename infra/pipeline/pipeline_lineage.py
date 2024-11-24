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
    def __init__(self, f_normatize_str_column: Callable, bg_logger):
        """
        Initialize the PipelineTransformer.

        Args:
            f_normatize_str_column: A callable function to normalize string columns.
            bg_logger: Logger instance for logging.
        """
        self.f_normatize_str_column = f_normatize_str_column
        self.bg_logger = bg_logger

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
        df['Invoice'] = self.f_normatize_str_column(
            self.bg_logger, df, 'Invoice', fillna_v='Unspecified'
        )
        df['StockCode'] = self.f_normatize_str_column(
            self.bg_logger, df, 'StockCode', fillna_v='Unspecified'
        )
        df['Description'] = self.f_normatize_str_column(
            self.bg_logger, df, 'Description', fillna_v='Unspecified'
        )
        df['Customer ID'] = self.f_normatize_str_column(
            self.bg_logger, df, 'Customer ID', fillna_v='Unspecified'
        )
        df['Country'] = self.f_normatize_str_column(
            self.bg_logger, df, 'Country', fillna_v='Unspecified'
        )

        # Specialized numeric dtypes, NaN for invalid values
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        # Specialized datetime to ISO 8601, NaT for invalid values
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%dT%H:%M:%S')

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
