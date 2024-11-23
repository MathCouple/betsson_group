"""
This module contains the main function for the invoices warehousing application.
It sets up paths, initializes logging, and logs execution time.


Attributes:
    root_path (str): The root directory of the application.
    dump_path (str): The directory where dump files are stored.
    utils_path (str): The directory where utility files are stored.
    _MIGRATE_DATABASE (bool): Flag indicating whether to prepare database
        Note: Migration will be used on the first execution of the code,
        but it will have no impact other than overhead for subsequent uses.
Functions:
    main_bg_invoice_warehousing():
    Main function of the application. Initializes logging and logs execution time.
main module for invoices warehousing
"""
import os
from utils._references import (
    get_current_utc_time,
    create_logger
)

# based on current file location, assuming it's root
root_path = os.path.dirname(os.path.abspath(__file__))
# paths that will have some static file in the application
dump_path = os.path.join(root_path, "dump")
utils_path = os.path.join(root_path, "utils")


_MIGRATE_DATABASE=True

def main_bg_invoice_warehousing():
    """
    Main function of the application.
    """

    _start_time = get_current_utc_time()
    bg_logger = create_logger(
        os.path.join(
            dump_path,
            "_warehousing.log"
        ),
    )

    bg_logger.info("This is a test message.")
    bg_logger.info("Execution time: %s", get_current_utc_time() - _start_time)


if __name__ == "__main__":
    main_bg_invoice_warehousing()
