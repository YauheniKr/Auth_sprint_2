from datetime import datetime
from uuid import UUID

from flask_jwt_extended import decode_token
from redis.client import StrictRedis as Redis

from src.db.redis_storage import redis_conn


class TokenStorageError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class RedisTokenStorage:
    def __init__(self):
        self.redis: Redis = redis_conn

    def jti_refresh_token(self, token: dict) -> None:
        current_refresh_token_jti = self.redis.get(str(token['sub']))

        if not current_refresh_token_jti:
            raise InvalidTokenError

        if current_refresh_token_jti != token['jti']:
            raise InvalidTokenError

        return

    def validate_access_token(self, access_token_jti: str) -> bool:
        return bool(self.redis.exists(access_token_jti))

    def invalidate_current_refresh_token(self, user_id: UUID) -> None:
        self.redis.delete(str(user_id))

    def set_refresh_token(self, token_jti: str, user_id: UUID) -> None:
        self.redis.set(name=str(user_id), value=token_jti)

    def add_token_to_database(self, decoded_token):

        jti = decoded_token["jti"]
        user_id = decoded_token["sub"]
        expires = datetime.fromtimestamp(decoded_token["exp"]) - datetime.now()
        self.redis.setex(name=user_id, value=jti, time=expires)
