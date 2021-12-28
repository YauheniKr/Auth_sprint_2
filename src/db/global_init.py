import sqlalchemy
import sqlalchemy.orm

from src.core.config import settings
from src.models.model_role import Role
from src.models.model_user import User
from src.models.model_base import ModelBase

__factory = None
username = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
host = settings.POSTGRES_HOST
port = settings.POSTGRES_PORT
database_name = settings.POSTGRES_DB


def global_init():
    global __factory

    full_file = f'{username}:{password}@{host}:{port}/{database_name}'
    conn_str = 'postgresql://' + full_file

    engine = sqlalchemy.create_engine(conn_str, echo=False, convert_unicode=True)
    ModelBase.metadata.create_all(engine)

    __factory = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=False, )


def create_session():
    global __factory

    if __factory is None:
        global_init()
    return __factory()
