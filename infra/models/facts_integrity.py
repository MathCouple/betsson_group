"""
Pydantic base validations for data integrity table
relates to facts
"""
from typing import Optional
from decimal import (
    Decimal,
    InvalidOperation
)
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
    - `quantity`: Integer representing the number of items (can be negative for returns).
    - `price`: Optional decimal representing the transaction price (non-negative or negative for adjustments).
    """
    transaction_id: str = Field(None, max_length=32)
    time_id: int = Field(..., ge=1)
    location_id: int = Field(..., ge=1)
    customer_id: Optional[int] = Field(None, ge=1)
    product_id: int = Field(..., ge=1)
    metadata_id: int = Field(..., ge=1)
    invoice_id: str
    quantity: int
    price: Optional[Decimal] = Field(None, description="Price must be a valid decimal value.")

    # pylint: disable=no-self-argument
    @field_validator("price", mode="before")
    def validate_price(cls, value):
        """
        Ensures that price is a valid decimal value or None.
        """
        if value is None:
            return value
        try:
            return Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError("Price must be a valid decimal value.")
