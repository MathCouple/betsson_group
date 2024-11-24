"""
This module contains the main function for the invoices warehousing application.
It sets up paths, initializes logging, and logs execution time.

It is meant to be run as orchestrator for the application.
"""
import os
from utils import (
    get_current_utc_time,
    create_logger,
    extract_7z
)
from infra.pipeline import (
    sanitize_column_data,
    sanitize_text,
    stage_base_transformer,
    NORMATIZE_LOCATION_MAP
)


# based on current file location, assuming it's root
root_path = os.path.dirname(os.path.abspath(__file__))


_MIGRATE_DATABASE=True

def main_bg_invoice_warehousing():
    """
    Main function of the application.
    """
    _start_time = get_current_utc_time()
    bg_logger = create_logger(
        os.path.join(root_path, "_warehousing.log"),
    )
    _ingestion_path = os.path.join(
        root_path,
        "ingestion"
    )

    # Extract 7z files
    extract_7z(bg_logger, _ingestion_path)

    # Load base data
    bg_logger.info("Loading base data...")
    base_df = pd.read_csv(
        os.path.join(
            _ingestion_path,
            'Invoices_Year_2009-2010.csv'
        ),
        sep=',',
        encoding='latin1',
        low_memory=False
    )

    bg_logger.info("This is a test message.")
    bg_logger.info("Execution time: %s", get_current_utc_time() - _start_time)


if __name__ == "__main__":
    main_bg_invoice_warehousing()
