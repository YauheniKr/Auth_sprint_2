import logging
from time import sleep

import redis

from tests.functional.settings import test_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_redis_availability():
    redis_client = redis.Redis(host=test_settings.REDIS_HOST, port=test_settings.REDIS_PORT)
    while True:
        try:
            redis_client.ping()
            logger.info("Redis Running")
            exit(0)
        except redis.exceptions.ConnectionError as e:
            logger.error(e)
            logger.error("Redis is not available. Sleep for 10 sec")
            sleep(10)
        else:
            redis_client.close()
            exit(1)


if __name__ == '__main__':
    check_redis_availability()
