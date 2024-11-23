"""
All fact models are defined here.

Models logic:
_schema_name - schema name
__tablename__ - name of the table
__table_args__ - Scheman name and Index for the table declarations
vars with Column use - columns of the table
"""
from sqlalchemy import (
    Column, Integer,
    Float, ForeignKey,
    Index
)

from . import Base


_SCHEMA_NAME = 'sales_warehousing'

class SalesFact(Base):
    """
    Represents the central fact table for sales transactions.

    Schema: sales_warehousing

    Attributes:
        sales_id (int): Primary key for the table.
        product_id (int): Foreign key linking to the product_dimension table.
        customer_id (int): Foreign key linking to the customer_dimension table.
        timestamp_id (int): Foreign key linking to the time_dimension table.
        region_id (int): Foreign key linking to the region_dimension table.
        quantity (int): Quantity of items sold in the transaction.
        price (float): Unit price of the product in the transaction.
    """
    __tablename__ = 'sales_fact'
    __table_args__ = (
        Index('idx_product_price', 'product_id', 'price'),
        Index('idx_customer_region', 'customer_id', 'region_id'),
        Index('idx_timestamp', 'timestamp_id'),
        # {'schema': f'{_SCHEMA_NAME}'},
    )

    sales_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    product_id = Column(
        Integer,
        ForeignKey('product_dimension.product_id'),
        nullable=False
    )
    customer_id = Column(
        Integer,
        ForeignKey('customer_dimension.customer_id'),
        nullable=True
    )
    timestamp_id = Column(
        Integer,
        ForeignKey('time_dimension.timestamp_id'),
        nullable=False
    )
    region_id = Column(
        Integer,
        ForeignKey('region_dimension.region_id'),
        nullable=False
    )
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
