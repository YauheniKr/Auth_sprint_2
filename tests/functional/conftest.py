import logging
import pytest

from tests.functional.settings import test_settings
from tests.functional.utils.global_init import create_session


@pytest.fixture(scope='session')
def postgres_session():
    session = create_session()
    yield session
    session.close()


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
        'password': '123',
        'email': 'fake@yamdb.ru'
    }
    user_test_data_2 = {
        'username': 'user2',
        'password': '123',
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

