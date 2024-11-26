"""
MSSQL Connection Handler
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


class MssqlConnector:
    """
    Class to manage database connections using SQLAlchemy.

    Attributes:
        logger: Logger instance for logging information.
        db_url: Database connection string.
        engine: SQLAlchemy Engine instance.
    
    Methods:
        connect: Creates the SQLAlchemy engine and establishes a connection to the database.
        get_connection_pid: Returns the session ID (SPID) of the current database connection.
        get_engine: Returns the SQLAlchemy engine.
    """

    def __init__(self, logger, db_url: str):
        """
        Initialize the DatabaseConnector with the database URL.

        :param logger: Logger instance for logging information.
        :param db_url: Database connection string.
        """
        self._logger = logger
        self.db_url = db_url
        self.engine = None

    def connect(self) -> Engine:
        """
        Creates the SQLAlchemy engine and establishes a connection to the database.

        :return: SQLAlchemy Engine instance.
        """
        try:
            self.engine = create_engine(self.db_url)
            with self.engine.connect() as connection: # pylint: disable=unused-variable
                self._logger.info("Connected to the database successfully.")
            self._logger.info("Engine created successfully.")
            return self.engine
        except SQLAlchemyError as e:
            self._logger.error("Failed to connect to the database: %s", str(e))
            raise RuntimeError("Error connecting to the database.") from e

    def get_connection_pid(self) -> int:
        """
        Returns the session ID (SPID) of the current database connection.

        :return: Session ID.
        """
        if self.engine is None:
            raise RuntimeError("Engine is not initialized. Please connect to the database first.")

        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT @@SPID AS session_id;"))
                spid = result.scalar()
                self._logger.info("Retrieved SPID: %s", spid)
                return spid
        except SQLAlchemyError as e:
            self._logger.error("Error retrieving connection SPID: %s", str(e))
            raise RuntimeError("Error retrieving connection SPID.") from e

    def get_engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine.

        :return: SQLAlchemy Engine instance.
        """
        if self.engine is None:
            raise RuntimeError("Engine is not initialized. Please connect to the database first.")
        return self.engine

    def close_connection(self):
        """
        Closes the database connection.

        :return: None
        """
        if self.engine is not None:
            self.engine.dispose()
            self._logger.info("Database connection closed.")
        else:
            self._logger.warning("Database connection is already closed.")

def create_warehouse_schema(engine):
    """
    Creates a schema in the database if it does not exist.
    Raises an error if the issue is connection-related.
    """
    with engine.begin() as connection:
        try:
            connection.execute(text("""
                CREATE SCHEMA sales_warehousing';
            """))
        except SQLAlchemyError as exc:
            try:
                connection.execute(text("""
                    IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'sales_warehousing')
                    BEGIN
                        EXEC('CREATE SCHEMA sales_warehousing');
                    END
                """))
            except SQLAlchemyError as inner_exc:
                raise RuntimeError("Error creating warehouse schema.") from inner_exc
