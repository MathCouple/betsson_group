"""
Pydantic base validations for data integrity table
relates to facts
"""
from pydantic import (
    BaseModel,
    Field
)
from typing import Optional
from datetime import date


class FactSalesTransactionValidation(BaseModel):
    """
    Validation model for transaction fact table. Validates:
    - `transaction_id`: Optional positive integer.
    - `time_id`: Mandatory positive integer linking to the time dimension.
    - `location_id`: Mandatory positive integer linking to the location dimension.
    - `customer_id`: Optional positive integer linking to the customer dimension.
    - `product_id`: Mandatory positive integer linking to the product dimension.
    - `metadata_id`: Mandatory positive integer linking to the metadata transactions.
    - `invoice_id`: Mandatory positive integer representing the invoice ID.
    - `quantity`: Integer representing the number of items (can be negative for returns).
    - `price`: Optional float representing the transaction price (can be negative for adjustments).
    """
    transaction_id: Optional[int] = Field(None, ge=1)
    time_id: int = Field(..., ge=1)
    location_id: int = Field(..., ge=1)
    customer_id: Optional[int] = Field(None, ge=1)
    product_id: int = Field(..., ge=1)
    metadata_id: int = Field(..., ge=1)
    invoice_id: str
    quantity: int
    price: Optional[float]
