from pydantic import BaseSettings
from pydantic.parse import Path

BASE_DIR = Path(__file__).resolve().parent
TESTDATA_DIR = Path(*[BASE_DIR / 'testdata' / 'data'])
SCHEMA_DIR = Path(*[BASE_DIR / 'testdata' / 'schema'])
UTILS_DIR = [BASE_DIR / 'utils']


class TestSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    # Настройки Elasticsearch
    ELASTIC_HOST: str = 'postgres'
    ELASTIC_PORT: int = 5432

    # Настройки сервиса
    SERVICE_HOST: str = 'auth_api'
    SERVICE_PORT: int = 8000

    # Настройки Postgres
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'movies'

    class Config:
        case_sensitive = True


test_settings = TestSettings()
