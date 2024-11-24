"""
This module contains the main function for the invoices warehousing application.
It sets up paths, initializes logging, and logs execution time.

It is meant to be run as orchestrator for the application.
"""
import os

import pandas as pd

from utils import (
    get_current_utc_time,
    create_logger,
    extract_7z,
    validate_file_exists
)

from infra.pipeline import (
    PipelineTransformer,
    sanitize_column_data
)


# based on current file location, assuming it's root
root_path = os.path.dirname(os.path.abspath(__file__))

# Parquet save base parameters
overall_stage_save_params = {
    'compression': 'snappy',
    'index': False
}

_MIGRATE_DATABASE = True


def main_bg_invoice_warehousing():
    """
    Main function of the application.
    """
    # Initialize base utilities
    _start_time = get_current_utc_time()
    bg_logger = create_logger(
        os.path.join(root_path, "_warehousing.log"),
    )
    _ingestion_path = os.path.join(
        root_path,
        "ingestion"
    )
    _ingestion_filename = 'Invoices_Year_2009-2010'

    # Validate compressed file existence
    validate_file_exists(
        bg_logger,
        os.path.join(_ingestion_path, f"{_ingestion_filename}.7z")
    )

    # Decompress file
    extract_7z(
        bg_logger,
        os.path.join(_ingestion_path, f"{_ingestion_filename}.7z"),
    )

    # Load base data
    _base_df_params = {
        'sep': ',',
        'encoding': 'latin1',
        'low_memory': False
    }
    base_df = pd.read_csv(
        os.path.join(_ingestion_path, f"{_ingestion_filename}.csv"),
        **_base_df_params
    )

    # Initialize the transformer
    transformer = PipelineTransformer(
        bg_logger=bg_logger
    )

    # Process stage I
    stage_i_df = transformer.stage_1(
        sanitize_column_data,
        base_df
    )
    transformer.save_parquet_stage(
        stage_i_df,
        os.path.join(root_path, "retail_stage_i.parquet"),
        **overall_stage_save_params
    )
    stage_i_df = None
    del stage_i_df

    # Generate warehouse-ready data for database
    # (Placeholder for future database migration logic)
    if _MIGRATE_DATABASE:
        bg_logger.info("Migrating warehouse-ready data to the database.")

    # Generate analysis and reports (future feature placeholders)

    # Logic for generating analysis and reports

    bg_logger.info("Execution time: %s", get_current_utc_time() - _start_time)


if __name__ == "__main__":
    main_bg_invoice_warehousing()
