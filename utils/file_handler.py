"""
Handles file-related operations
"""
from datetime import datetime
import os

import py7zr


def extract_7z(bg_logger, file_path):
    """
    Extracts a 7z file to the same directory as the compressed file.

    :param bg_logger: initialized logger
    :param file_path: Path to the 7z file to extract.
    """
    # Record start time
    start_time = datetime.now()

    # Get extraction directory
    extract_dir = os.path.dirname(file_path)

    # Extract the 7z file
    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(path=extract_dir)

    # Calculate extraction duration
    duration = datetime.now() - start_time

    # Log success message with extraction details
    bg_logger.info(
        "Data successfully extracted to directory %s. Duration: %s",
        extract_dir, duration
    )
    extract_dir = None
    del extract_dir


def validate_file_exists(bg_logger, file_path):
    """
    Validates if a file exists.

    :param file_path: Path to the file to validate.
    :return: True if the file exists, False otherwise.
    """
    if not os.path.exists(file_path):
        bg_logger.critical("File %s does not exist", file_path)
        raise FileNotFoundError(f"File {file_path} does not exist")
