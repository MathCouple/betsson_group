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
    Column, Integer, String, Date, Boolean
)
from sqlalchemy.orm import (
    relationship
)


from . import Base


_SCHEMA_NAME = 'sales_warehousing'


class DimTime(Base):
    """
    Represents the time dimension table for the data warehouse.

    Attributes:
        time_id (int): Primary key for the time dimension.
        date (Date): The full date (YYYY-MM-DD).
        year (int): The year of the transaction (e.g., 2024).
        quarter (int): The quarter of the year (1-4).
        month (int): The month of the year (1-12).
        day (int): The day of the month (1-31).
        week (int): The week of the year (1-53).
        day_of_week (str): Name of the day (e.g., "Monday").
        hour (int): Optional hour of the transaction (0-23).
        minute (int): Optional minute of the transaction (0-59).
        second (int): Optional second of the transaction (0-59).
    """
    __tablename__ = 'dim_time'
    __table_args__ = {'schema': _SCHEMA_NAME}

    time_id = Column(String, primary_key=True)
    date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    day_of_week = Column(String(10), nullable=False)
    hour = Column(Integer, nullable=True)
    minute = Column(Integer, nullable=True)
    second = Column(Integer, nullable=True)

    transactions = relationship("FactSalesTransaction", back_populates="time")


class DimLocation(Base):
    """
    Represents the location dimension table for the data warehouse.

    Attributes:
        location_id (int): Primary key for the location dimension.
        location_name (str): Name of the location where the transaction occurred.
    """
    __tablename__ = 'dim_location'
    __table_args__ = {'schema': _SCHEMA_NAME}

    location_id = Column(String, primary_key=True)
    location_name = Column(String(255), nullable=True)

    transactions = relationship("FactSalesTransaction", back_populates="location")


class DimCustomer(Base):
    """
    Represents the customer dimension table for the data warehouse.

    Attributes:
        customer_id (int): Primary key for the customer dimension.
        customer_code (str): Unique code identifying the customer, if available.
        is_known_customer (bool): Indicates whether the customer is known or anonymous.
    """
    __tablename__ = 'dim_customer'
    __table_args__ = {'schema': _SCHEMA_NAME}

    customer_id = Column(String, primary_key=True)
    customer_code = Column(String(255), nullable=True)
    is_known_customer = Column(Boolean, nullable=False)

    transactions = relationship("FactSalesTransaction", back_populates="customer")


class DimProduct(Base):
    """
    Represents the product dimension table for the data warehouse.

    Attributes:
        product_id (int): Primary key for the product dimension.
        stock_code (str): Unique code identifying the product stock.
        description (str): Description of the product.
    """
    __tablename__ = 'dim_product'
    __table_args__ = {'schema': _SCHEMA_NAME}

    product_id = Column(String, primary_key=True)
    stock_code = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    transactions = relationship("FactSalesTransaction", back_populates="product")


class DimMetadataTransaction(Base):
    """
    Represents the transaction metadata table for the data warehouse.

    Attributes:
        metadata_id (int): Primary key for the metadata transactions table.
        transaction_description (str): Description of the transaction type or reason.
        transaction_category (str): Category of the transaction
        (e.g., "sale", "adjustment", "return", "fee").
    """
    __tablename__ = 'dim_metadata_transactions'
    __table_args__ = {'schema': 'sales_warehousing'}

    metadata_id = Column(String, primary_key=True)
    transaction_description = Column(String(255), nullable=False)
    transaction_category = Column(String(50), nullable=False)

    transactions = relationship("FactSalesTransaction", back_populates="metadata_transactions")
