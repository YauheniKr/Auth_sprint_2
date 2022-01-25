import hashlib
from datetime import timedelta

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    env_file = load_dotenv()
    # Настройки Redis
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    # Настройки Postgres
    POSTGRES_HOST: str = '192.168.23.132'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'postgres'
    POSTGRES_DB: str = 'movies'

    # Настройки Flask
    SECRET_KEY = hashlib.md5('super_secret'.encode()).hexdigest()
    ACCESS_EXPIRES = timedelta(minutes=60)
    REFRESH_EXPIRES = timedelta(days=15)

    # Настройки Yandex
    YANDEX_ID: str
    YANDEX_PASSWORD: str

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
