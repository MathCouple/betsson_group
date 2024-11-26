"""
Pydantic base validations for data integrity table
relates to dimensions
"""
from pydantic import (
    BaseModel,
    Field
)
from typing import Optional
import pandas as pd


class DimTimeValidation(BaseModel):
    """
    Validation model for time dimension. Validates temporal data, ensuring:
    - `time_id`: Optional positive integer.
    - `date`: Mandatory date field in YYYY-MM-DD format.
    - `year`: Year between 1900 and 2100.
    - `quarter`: Quarter of the year (1-4).
    - `month`: Month of the year (1-12).
    - `day`: Day of the month (1-31).
    - `week`: Week of the year (1-53).
    - `day_of_week`: String with a max length of 10 characters (e.g., "Monday").
    - `hour`, `minute`, `second`: Optional time components with valid ranges.
    """
class DimTimeGenerator(BaseModel):
    """
    Generates the dim_time table.
    """
    def generate_table(self) -> pd.DataFrame:
        """
        Creates the dim_time table from the preprocessed data.
        """
        self.df['date'] = self.df['invoice_date'].dt.date
        self.df['hour'] = self.df['invoice_date'].dt.hour
        self.df['minute'] = self.df['invoice_date'].dt.minute
        self.df['second'] = self.df['invoice_date'].dt.second

        dim_time = self.df[['date', 'invoice_date', 'year', 'quarter', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second']].drop_duplicates()

        dim_time['time_id'] = range(1, len(dim_time) + 1)

        return dim_time

class DimLocationValidation(BaseModel):
    """
    Validation model for location dimension. Validates:
    - `location_id`: Optional positive integer.
    - `location_name`: Mandatory string with a max length of 255 characters.
    """
    location_id: Optional[int] = Field(None, ge=1)
    location_name: Optional[str] = Field(None, max_length=255)

class DimCustomerValidation(BaseModel):
    """
    Validation model for customer dimension. Validates:
    - `customer_id`: Mandatory positive integer.
    - `customer_code`: Optional string with a max length of 255 characters.
    - `is_known_customer`: Boolean indicating if the customer is identified.
    """
    customer_id: int
    customer_code: Optional[str] = Field(None, max_length=255)
    is_known_customer: bool

class DimProductValidation(BaseModel):
    """
    Validation model for product dimension. Validates:
    - `product_id`: Optional positive integer.
    - `stock_code`: Mandatory string with a max length of 255 characters.
    - `description`: Mandatory string with a max length of 255 characters.
    """
    product_id: Optional[int] = Field(None, ge=1)
    stock_code: str = Field(..., max_length=255)
    description: str = Field(..., max_length=255)

class DimMetadataTransactionValidation(BaseModel):
    """
    Validation model for transaction metadata. Validates:
    - `metadata_id`: Optional positive integer.
    - `transaction_description`: Mandatory string with a max length of 255 characters.
    - `transaction_category`: Mandatory string with a max length of 50 characters
      indicating the type of transaction (e.g., 'sale', 'adjustment', 'return').
    """
    metadata_id: Optional[int] = Field(None, ge=1)
    transaction_description: str = Field(..., max_length=255)
    transaction_category: str = Field(..., max_length=50)
