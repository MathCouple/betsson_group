"""
Pydantic base validations for data integrity table
relates to facts
"""
from typing import Optional
from decimal import (
    Decimal,
    InvalidOperation
)
import numpy as np
from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class FactSalesTransactionValidation(BaseModel):
    """
    Validation model for transaction fact table. Validates:
    - `transaction_id`: Optional hash string (up to 32 characters).
    - `time_id`: Mandatory positive integer linking to the time dimension.
    - `location_id`: Mandatory positive integer linking to the location dimension.
    - `customer_id`: Optional positive integer linking to the customer dimension.
    - `product_id`: Mandatory positive integer linking to the product dimension.
    - `metadata_id`: Mandatory positive integer linking to the metadata transactions.
    - `invoice_id`: Mandatory string representing the invoice ID.
    - `quantity`: Integer representing the number of items
    (can be negative for returns).
    - `price`: Optional decimal representing the transaction price
    (non-negative or negative for adjustments).
    """
    transaction_id: str = Field(..., max_length=32)
    time_id: str = Field(..., max_length=32)
    location_id: Optional[str] = Field(None, max_length=32)
    customer_id: Optional[str] = Field(None, max_length=32)
    product_id: str = Field(None, max_length=32)
    metadata_id: str = Field(None, max_length=32)
    invoice_id: str
    quantity: int
    price: Optional[Decimal] = Field(None, description="Price must be a valid decimal value.")
    # pylint: disable=no-self-argument
    @field_validator("price", mode="before")
    def validate_price(cls, value):
        """
        Ensures that price is a valid decimal value or None.
        """
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return None
        try:
            return Decimal(value)
        except (ValueError, InvalidOperation) as e:
            raise ValueError("Price must be a valid decimal value.") from e
