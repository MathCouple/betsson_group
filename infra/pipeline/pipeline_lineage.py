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

def stage_base_transformer(f_normatize_str_column: Callable, bg_logger, df) -> pd.DataFrame:
    """
    -- Not all parameters is being visually "typed". Callable are not usually intuitive. --
    Applies the first stage of transformations to the data.
    Args:
        bg_logger: Logger instance for logging.
        df: DataFrame containing the data.
    Returns:
        The transformed DataFrame.
    """
    start_time = datetime.now()

    # specialized string dtypes
    df['Invoice'] = f_normatize_str_column(bg_logger, df, 'Invoice', fillna_v='Unspecified')
    df['StockCode'] = f_normatize_str_column(bg_logger, df, 'StockCode', fillna_v='Unspecified')
    df['Description'] = f_normatize_str_column(bg_logger, df, 'Description', fillna_v='Unspecified')
    df['Customer ID'] = f_normatize_str_column(bg_logger, df, 'Customer ID', fillna_v='Unspecified')
    df['Country'] = f_normatize_str_column(bg_logger, df, 'Country', fillna_v='Unspecified')

    # specialized numeric dtypes, NaN for invalid values
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # specialized datetime to ISO 8601, NaT for invalid values
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    bg_logger.info("Stage Base transformations completed in %s", str(datetime.now() - start_time))
    return df
