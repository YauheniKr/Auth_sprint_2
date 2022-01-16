from datetime import datetime

import pytest
from flask import Flask
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, decode_token)
from werkzeug.security import generate_password_hash

from tests.functional.settings import test_settings as settings
from tests.functional.utils.global_init import create_session
from tests.functional.utils.redis_storage import redis_conn


@pytest.fixture(scope='session')
def postgres_session():
    session = create_session()
    yield session
    session.close()


def flask_app():
    app = Flask(__name__)
    JWTManager(app)
    app.config.update({"JWT_SECRET_KEY": settings.SECRET_KEY, "JWT_ACCESS_TOKEN_EXPIRES": settings.ACCESS_EXPIRES,
                       "JWT_REFRESH_TOKEN_EXPIRES": settings.REFRESH_EXPIRES})
    return app.app_context().push()


@pytest.fixture(scope='function')
def redis_session():
    session = redis_conn
    yield session
    session.flushall()


@pytest.fixture(scope='session')
def role(postgres_session):
    from tests.functional.models.model_role import Role
    test_data = {
        "description": "test role",
        "role_name": "user_test",
        "role_weight": 111
    }
    role = Role(**test_data)
    postgres_session.query(Role).delete()
    postgres_session.commit()
    postgres_session.add(role)
    postgres_session.commit()
    yield role
    postgres_session.query(Role).delete()
    postgres_session.commit()


@pytest.fixture(scope='session')
def roles(postgres_session):
    from tests.functional.models.model_role import Role
    test_data_1 = {
        "description": "test role",
        "role_name": "user_test",
        "role_weight": 111
    }
    test_data_2 = {
        "description": "test role 1",
        "role_name": "user_test_2",
        "role_weight": 112
    }
    test_datas = [test_data_1, test_data_2]
    roles = [Role(**test_data) for test_data in test_datas]
    postgres_session.query(Role).delete()
    postgres_session.commit()
    postgres_session.bulk_save_objects(roles, return_defaults=True)
    postgres_session.commit()
    yield roles
    postgres_session.query(Role).delete()
    postgres_session.commit()


@pytest.fixture(scope='session')
def users(postgres_session):
    from tests.functional.models.model_user import User
    user_test_data_1 = {
        'username': 'user1',
        'password': generate_password_hash('123', method='sha256'),
        'email': 'fake@yamdb.ru'
    }
    user_test_data_2 = {
        'username': 'user2',
        'password': generate_password_hash('123', method='sha256'),
        'email': 'fake@yamdb.com'
    }
    users = [user_test_data_1, user_test_data_2]
    users = [User(**test_data) for test_data in users]
    postgres_session.query(User).delete()
    postgres_session.commit()
    postgres_session.bulk_save_objects(users, return_defaults=True)
    postgres_session.commit()
    yield users
    postgres_session.query(User).delete()
    postgres_session.commit()


@pytest.fixture(scope='function')
def tokens(users, redis_session):
    user_id = str(users[0].id)
    flask_app()
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    token = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    decoded_token = decode_token(refresh_token)
    jti = decoded_token["jti"]
    expires = datetime.fromtimestamp(decoded_token["exp"]) - datetime.now()
    redis_session.setex(name=str(users[0].id), value=jti, time=expires)
    return token


@pytest.fixture(scope='function')
def admin_tokens(users, redis_session):
    user_id = str(users[1].id)
    flask_app()
    access_token = create_access_token(identity=user_id, additional_claims={"is_administrator": True})
    refresh_token = create_refresh_token(identity=user_id, additional_claims={"is_administrator": True})
    token = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    decoded_token = decode_token(refresh_token)
    jti = decoded_token["jti"]
    expires = datetime.fromtimestamp(decoded_token["exp"]) - datetime.now()
    redis_session.setex(name=str(users[1].id), value=jti, time=expires)
    return token
