import logging
from time import sleep

import psycopg2

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_postgres_availability():
    while True:
        try:
            db = psycopg2.connect(f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER}"
                                  f" host={settings.POSTGRES_HOST} password={settings.POSTGRES_PASSWORD}")
            logger.info("Postgres Running")
            exit(0)
        except psycopg2.Error as e:
            logger.info(e)
            logger.error("Postgres is not available. Sleep for 10 sec")
            sleep(10)
        else:
            db.close()
            exit(1)


if __name__ == '__main__':
    check_postgres_availability()
