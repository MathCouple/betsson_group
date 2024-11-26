"""
Handler module related to database migration.

Setting up the database schema and indexes.

INDEX_DEFINITIONS = {
    'table_name': [
        {'name': 'index_name', 'columns': ['column1', 'column2']}
    ]
}
"""
from infra.handlers import DatabaseConnector