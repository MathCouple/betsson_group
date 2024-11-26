"""
This module contains the metadata for the pipeline handlers.

It could be a OOP Enum, but for simplicity, it is a dictionary.
"""
from infra.models.dims_integrity import (
    DimTimeValidation,
    DimLocationValidation,
    DimCustomerValidation,
    DimProductValidation,
    DimMetadataTransactionValidation

)
from infra.models.facts_integrity import (
    FactSalesTransactionValidation
)

NORMATIZE_LOCATION_MAP = {
    "USA": "United States",
    "US": "United States",
    "UK": "United Kingdom",
    "EIRE": "Ireland",
    "RSA": "South Africa",
}


CLOUD_LOST_PRODUCTS_WORDS = [
    'damage', 'wet', 'MIA', 'smashed', 'missing', 'missed',
    'lost', 'crushed', 'broken', 'bad quality',
    'discoloured', 'rotting', 'damp and rusty',
    'unsellable', 'dirty', 'display', 'cant find',
    'debt', 'wrong', '?????', 'donated', 'rusty', 'damges',
    'found', 'gone', 'temp', 'phil said so', 'error',
    'eurobargain', 'broken', 'poor quality', '?sold individually?',
]

STAGE_III_COLUMNS = [
    'invoice', 'stock_code', 'description',
    'quantity', 'invoice_date', 'price',
    'customer_id', 'country', 'product_return',
    'lost_sales', 'financial_details',
    'maintenance_adjustment']

validation_models = {
    "dim_time": DimTimeValidation,
    "dim_location": DimLocationValidation,
    "dim_product": DimProductValidation,
    "dim_customer": DimCustomerValidation,
    "dim_metadata_transactions": DimMetadataTransactionValidation,
    "fact_sales_transactions": FactSalesTransactionValidation,
}
