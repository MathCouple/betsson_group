"""
Pydantic base validations for data integrity table
relates to dimensions
"""
from pydantic import (
    BaseModel,
    Field
)
from typing import Optional
from datetime import date


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
    time_id: Optional[int] = Field(None, ge=1)
    date: date
    year: int = Field(..., ge=1900, le=2100)
    quarter: int = Field(..., ge=1, le=4)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    week: int = Field(..., ge=1, le=53)
    day_of_week: str = Field(..., max_length=10)
    hour: Optional[int] = Field(None, ge=0, le=23)
    minute: Optional[int] = Field(None, ge=0, le=59)
    second: Optional[int] = Field(None, ge=0, le=59)

class DimLocationValidation(BaseModel):
    """
    Validation model for location dimension. Validates:
    - `location_id`: Optional positive integer.
    - `location_name`: Mandatory string with a max length of 255 characters.
    """
    location_id: Optional[int] = Field(None, ge=1)
    location_name: str = Field(..., max_length=255)

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
