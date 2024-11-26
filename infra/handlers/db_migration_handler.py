"""
Database migrations
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import CreateSchema, MetaData
from sqlalchemy.engine.reflection import Inspector
from infra.models import Base


def __ensure_schemas_and_tables(bg_logger, connection):
    """
    Ensure all schemas and tables defined in the SQLAlchemy models exist.
    """
    inspector = Inspector.from_engine(connection)

    # Ensure schemas exist
    existing_schemas = inspector.get_schema_names()
    for table in Base.metadata.sorted_tables:
        schema = table.schema
        if schema and schema not in existing_schemas:
            connection.execute(CreateSchema(schema))
        bg_logger.info("Schema %s exists", schema)
    # Create tables if they do not exist
    Base.metadata.create_all(bind=connection)


def __drop_schemas_and_tables(bg_logger, connection):
    """
    Drop all tables and schemas defined in the SQLAlchemy models.
    """
    inspector = Inspector.from_engine(connection)

    # Drop all tables in reverse order
    Base.metadata.drop_all(bind=connection)

    # Drop schemas
    for table in Base.metadata.sorted_tables:
        schema = table.schema
        if schema and schema in inspector.get_schema_names():
            connection.execute(f"DROP SCHEMA {schema}")
            bg_logger.info("Schema %s dropped", schema)

def migrate_database(bg_logger, engine):
    """
    Migrate data using the provided engine.
    """
    bg_logger.info("Migrating database")
    with engine.connect() as connection:
        with connection.begin():
            __drop_schemas_and_tables(bg_logger, connection)
            __ensure_schemas_and_tables(bg_logger, connection)
    bg_logger.info("Database migration completed")
