import hashlib
from datetime import timedelta

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    # Настройки сервиса
    SERVICE_HOST: str = 'auth_api'
    SERVICE_PORT: int = 8000

    # Настройки Postgres
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'movies'

    # Настройки Flask
    SECRET_KEY = hashlib.md5('super_secret'.encode()).hexdigest()
    ACCESS_EXPIRES = timedelta(minutes=60)
    REFRESH_EXPIRES = timedelta(days=15)

    class Config:
        case_sensitive = True


test_settings = TestSettings()
