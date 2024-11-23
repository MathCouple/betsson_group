"""
All Dimensional models are defined here.

As well their possible "indexes"


Models logic:
_schema_name - schema name
__tablename__ - name of the table
__table_args__ - Scheman name and Index for the table declarations
vars with Column use - columns of the table
"""
from sqlalchemy import (
    Column, Integer,
    ForeignKey, String,
    Index
)

from . import Base


_SCHEMA_NAME = 'sales_warehousing'

class TimeDimension(Base):
    """
    Represents the time dimension table with timestamp granularity.

    Schema: sales_warehousing

    Attributes:
        timestamp_id (int): Surrogate key for unique timestamps (format: YYYYMMDDHHMMSS).
        year (int): Year of the transaction.
        quarter (int): Quarter of the year (1-4).
        month (int): Month of the year (1-12).
        day (int): Day of the month (1-31).
        hour (int): Hour of the day (0-23).
        minute (int): Minute of the hour (0-59).
        second (int): Second of the minute (0-59).
    """
    __tablename__ = 'time_dimension'
    __table_args__ = (
        Index('idx_date', 'year', 'month', 'day'),
        Index('idx_time', 'hour', 'minute', 'second'),
        # {'schema': f'{_SCHEMA_NAME}'}
    )

    timestamp_id = Column(Integer, primary_key=True, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=True)
    minute = Column(Integer, nullable=True)

class ProductDimension(Base):
    """
    Represents the product dimension table.

    Schema: sales_warehousing

    Attributes:
        product_id (int): Primary key for the table.
        stock_code (str): Unique identifier for the product.
        description (str): Description of the product.
        category (str): Category or grouping of the product.
    """
    __tablename__ = 'product_dimension'
    __table_args__ = (
        Index('idx_stock_code', 'stock_code'),
        # {'schema': f'{_SCHEMA_NAME}'}

    )

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)

class CustomerDimension(Base):
    """
    Represents the customer dimension table.

    Schema: sales_warehousing

    Attributes:
        customer_id (int): Primary key for the table.
        customer_name (str): Name of the customer.
        region_id (int): Foreign key linking to the region_dimension table.
    """
    __tablename__ = 'customer_dimension'
    __table_args__ = (
        Index('idx_customer_region', 'customer_id', 'region_id'),
        #{'schema': f'{_SCHEMA_NAME}'}
    )

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100), nullable=True)
    region_id = Column(
        Integer,
        ForeignKey('region_dimension.region_id'),
        nullable=True
    )

class RegionDimension(Base):
    """
    Represents the region dimension table.

    Schema: sales_warehousing

    Attributes:
        region_id (int): Primary key for the table.
        country (str): Name of the country or region.
    """
    __tablename__ = 'region_dimension'
    __table_args__ = (
        Index('idx_country', 'country'),
        # {'schema': f'{_SCHEMA_NAME}'}
    )

    region_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False, unique=True)
