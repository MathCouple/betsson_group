"""
MSSQL Connection Handler
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class DatabaseConnector:
    """
    Class to manage database connections using SQLAlchemy.

    Attributes:
        logger: Logger instance for logging information.
        db_url: Database connection string.
        engine: SQLAlchemy Engine instance.
    
    Methods:
        connect: Creates the SQLAlchemy engine and establishes a connection to the database.
        get_connection_pid: Returns the PID of the current database connection.
        get_engine: Returns the SQLAlchemy engine.
    
    Use example:
        >>> from sqlalchemy.engine import Engine
        >>> from infra.handlers.mssql_handler import DatabaseConnector
        >>> db_connector = DatabaseConnector(logger, db_url)
        >>> engine: Engine = db_connector.connect()
        >>> connection_pid = db_connector.get_connection_pid()
        >>> engine = db_connector.get_engine()
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
            with self.engine.connect() as connection:
                self._logger.info(
                    "Connected to the database successfully. PID: %s",
                    connection.connection.connection.pid
                )
            return self.engine
        except SQLAlchemyError as e:
            self._logger.error("Failed to connect to the database: %s", str(e))
            raise RuntimeError("Error connecting to the database.") from e

    def get_connection_pid(self) -> int:
        """
        Returns the PID of the current database connection.

        :return: Connection PID.
        """
        if self.engine is None:
            raise RuntimeError("Engine is not initialized. Please connect to the database first.")

        try:
            with self.engine.connect() as connection:
                return connection.connection.connection.pid
        except SQLAlchemyError as e:
            self._logger.error("Error retrieving connection PID: %s", str(e))
            raise RuntimeError("Error retrieving connection PID.") from e

    def get_engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine.

        :return: SQLAlchemy Engine instance.
        """
        if self.engine is None:
            raise RuntimeError("Engine is not initialized. Please connect to the database first.")
        return self.engine
