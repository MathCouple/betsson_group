"""
All fact models are defined here.

Models logic:
_schema_name - schema name
__tablename__ - name of the table
__table_args__ - Scheman name and Index for the table declarations
vars with Column use - columns of the table
"""
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship


from . import Base


_SCHEMA_NAME = 'sales_warehousing'


class FactSalesTransaction(Base):
    """
    Represents the fact table for transactions in the data warehouse.

    Attributes:
        transaction_id (int): Primary key for the transaction fact table.
        time_id (int): Foreign key referencing the time dimension.
        location_id (int): Foreign key referencing the location dimension.
        customer_id (int): Foreign key referencing the customer dimension (nullable).
        product_id (int): Foreign key referencing the product dimension.
        metadata_id (int): Foreign key referencing the metadata transactions dimension.
        invoice_id (int): Unique identifier for the invoice.
        quantity (int): Number of units involved in the transaction.
        price (float): Price per unit of the product (nullable; may include refunds or adjustments).
    """
    __tablename__ = 'fact_sales_transactions'
    __table_args__ = {'schema': _SCHEMA_NAME}

    transaction_id = Column(String, primary_key=True)
    time_id = Column(Integer, ForeignKey('sales_warehousing.dim_time.time_id'), nullable=False)
    location_id = Column(
        String,
        ForeignKey('sales_warehousing.dim_location.location_id'), nullable=False
    )
    customer_id = Column(
        String, ForeignKey('sales_warehousing.dim_customer.customer_id'), nullable=True
    )
    product_id = Column(
        String, ForeignKey('sales_warehousing.dim_product.product_id'), nullable=False
    )
    metadata_id = Column(
        String, ForeignKey('sales_warehousing.dim_metadata_transactions.metadata_id'), nullable=False
    )
    invoice_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=True)
    metadata_transactions = relationship("DimMetadataTransaction", back_populates="transactions")
