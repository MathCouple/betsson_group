from sqlalchemy import create_engine
from infra.models import Base
from infra.models.fact import *
from infra.models.dim import *

def initialize_database():
    """
    Cria o banco de dados SQLite e inicializa as tabelas definidas nos modelos.
    """
    engine = create_engine("sqlite:///test.db")

    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso no banco de dados!")

if __name__ == "__main__":
    initialize_database()
