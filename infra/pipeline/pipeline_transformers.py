"""
Module specialized on data transformation functions.
"""
import re
import unicodedata
from datetime import datetime



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
