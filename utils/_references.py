"""
_references module


- internal General utils configs
"""
from datetime import (
    datetime,
    timezone
)
import logging
import uuid



# pylint: disable=C0103
class __UUIDFilter(logging.Filter):
    """
    Internal utils
    Filter that adds a UUID4 to the log record.
    """
    def filter(self, record):
        record.uuid4 = uuid.uuid4()
        return True


def get_current_utc_time():
    """
    Returns the current UTC time.
    """
    return datetime.now(timezone.utc)

def create_logger(log_file=None):
    """
    Creates a logger that writes messages to a file and writes them to the console.

    :param log_file: Name of the log file.
    :return: Configured logger.
    """
    # Logger creation
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Custom log format with UTC timestamp and UUID4
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(funcName)s] - [%(uuid4)s] - %(message)s',
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    # Force the UTC time to appear in all handlers
    logging.Formatter.converter = lambda *args: datetime.now(timezone.utc).timetuple()

    uuid_filter = __UUIDFilter()
    logger.addFilter(uuid_filter)

    # File writer handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger
