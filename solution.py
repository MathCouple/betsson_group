"""
This module contains the main function for the invoices warehousing application.
It sets up paths, initializes logging, and logs execution time.

It is meant to be run as orchestrator for the application.
"""
import os

import pandas as pd
import dotenv

from utils import (
    get_current_utc_time,
    create_logger,
    extract_7z,
    validate_file_exists
)

from infra.pipeline import (
    PipelineTransformer,
    sanitize_column_data,
    sanitize_text
)
from infra.handlers import (
    MssqlConnector,
    create_warehouse_schema
)
from infra.models import Base

# Load environment variables
dotenv.load_dotenv()


# based on current file location, assuming it's root
root_path = os.path.dirname(os.path.abspath(__file__))

# Parquet save base parameters
overall_stage_save_params = {
    'compression': 'snappy',
    'index': False
}
bg_logger = create_logger(
    os.path.join(root_path, "_warehousing.log"),
)

# if not checked, it will be created locally
_MIGRATE_DATABASE = True

MSSQL_WAREHOUSE_URL=os.getenv("MSSQL_WAREHOUSE_URL")

if not MSSQL_WAREHOUSE_URL:
    bg_logger.warning(
        "The environment variable 'MSSQL_WAREHOUSE_URL'"
    )
    _MIGRATE_DATABASE = False

def main_bg_invoice_warehousing():
    """
    Main function of the application.
    """
    # Initialize base utilities
    _start_time = get_current_utc_time()
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
        bg_logger=bg_logger,
        f_sanitize_text=sanitize_text,
        f_sanitize_column_data=sanitize_column_data
    )

    # every stage can be saved to speed up the process
    # starting from the previous stage if it exists
    stage_i_df = transformer.stage_1(
        base_df
    )

    stage_ii_df = transformer.stage_2(
        stage_i_df
    )

    stage_iii_df = transformer.stage_3(
        stage_ii_df
    )

    # transformer.save_parquet_stage(
    #     stage_iii_df, 'stage_iii.parquet'
    # )
    # stage_iii_df = pd.read_parquet(
    #     'stage_iii.parquet'
    # )

    if _MIGRATE_DATABASE:
        try:
            mssql_instance = MssqlConnector(
                bg_logger,
                MSSQL_WAREHOUSE_URL
            )
            engine = mssql_instance.connect()
            create_warehouse_schema(engine)
            Base.metadata.create_all(bind=engine)
            transformer.generates_dw_tables(
                stage_iii_df,
                engine
            )

        except Exception as e:  # pylint: disable=broad-except
            bg_logger.error("Error migrating/saving data to the warehouse: %s", e)
        finally:
            mssql_instance.close_connection()
    else:
        bg_logger.info("Saving stage III data locally.")
        bg_logger.warning(
            "Note: DW Will only be generated in MSSQL"
            ". To follow the process, please, read the README requirements to run this project"
        )

        transformer.save_parquet_stage(
            stage_iii_df,
            'stage_iii.parquet',
            **overall_stage_save_params
        )


    bg_logger.info("Execution time: %s", get_current_utc_time() - _start_time)


if __name__ == "__main__":
    main_bg_invoice_warehousing()
