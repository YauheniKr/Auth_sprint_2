from redis.client import StrictRedis

from tests.functional.settings import test_settings as settings

redis_conn = StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)
