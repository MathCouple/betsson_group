"""
Handler module related to database migration.

Setting up the database schema and indexes.

INDEX_DEFINITIONS = {
    'table_name': [
        {'name': 'index_name', 'columns': ['column1', 'column2']}
    ]
}
"""
from infra.models.fact import SalesFact
from infra.models.dim import (
    TimeDimension,
    ProductDimension,
    CustomerDimension,
    RegionDimension,
)



# relation to create the indexes tables
INDEX_DEFINITIONS = {
    "sales_fact": [
        {"name": "idx_product_price", "columns": ["product_id", "price"]},
        {"name": "idx_customer_region", "columns": ["customer_id", "region_id"]},
        {"name": "idx_timestamp", "columns": ["timestamp_id"]},
    ],
    "time_dimension": [
        {"name": "idx_date", "columns": ["year", "month", "day"]},
        {"name": "idx_time", "columns": ["hour", "minute", "second"]},
    ],
    "product_dimension": [
        {"name": "idx_stock_code", "columns": ["stock_code"]},
    ],
    "customer_dimension": [
        {"name": "idx_customer_region", "columns": ["customer_id", "region_id"]},
    ],
    "region_dimension": [
        {"name": "idx_country", "columns": ["country"]},
    ],
}
