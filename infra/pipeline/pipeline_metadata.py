"""
This module contains the metadata for the pipeline handlers.

It could be a OOP Enum, but for simplicity, it is a dictionary.
"""
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
    'debt', 'wrong', '?????', 'donated', 'rusty' 'damges',
    'found', 'gone', 'temp', 'phil said so', 'error',
    'eurobargain', 'broken', 'poor quality', '?sold individually?',
]
