import json
from http import HTTPStatus

import requests
from flask_jwt_extended import decode_token


class TestsUserApi:

    def test_user_create(self):
        url = f'http://192.168.88.131:8000/api/v1/auth/user/signup'
        data = {
            'username': 'user111',
            'password': '12311',
            'email': 'fake@yamdb.ya'
        }
        json_data = json.dumps(data)
        user_answer = requests.post(url, data=json_data)
        assert user_answer.status_code == HTTPStatus.OK

    def test_user_update(self, users, tokens):
        url = f'http://auth_api:8000/api/v1/auth/user/me'
        data = {'email': 'fake@yamdb.fake'}
        access = tokens['access_token']
        headers = {
            'Authorization': f'Bearer {access}',
            'Content-Type': 'application/json'
        }
        json_data = json.dumps(data)
        user_answer = requests.patch(url, data=json_data, headers=headers)
        assert user_answer.status_code == HTTPStatus.OK

    def test_user_login(self, users):
        url = f'http://auth_api:8000/api/v1/auth/user/login'
        data = {
            'username': 'user1',
            'password': '123',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        json_data = json.dumps(data)
        user_answer = requests.post(url, data=json_data, headers=headers)
        assert user_answer.status_code == HTTPStatus.OK
        assert 'access_token' in user_answer.json()
        assert 'refresh_token' in user_answer.json()

    def test_user_logout(self, users, tokens, redis_session):
        url = f'http://auth_api:8000/api/v1/auth/user/logout'
        access = tokens['access_token']
        headers = {
            'Authorization': f'Bearer {access}',
            'Content-Type': 'application/json'
        }
        user_answer = requests.get(url, headers=headers)
        jti = redis_session.get(str(users[0].id))
        assert user_answer.status_code == HTTPStatus.OK
        assert decode_token(access)['jti'] == jti

    def test_user_refresh_token(self, users, tokens, redis_session):
        url = f'http://auth_api:8000//api/v1/auth/token/refresh'
        refresh = tokens['refresh_token']
        headers = {
            'Authorization': f'Bearer {refresh}',
            'Content-Type': 'application/json'
        }
        user_answer = requests.post(url, headers=headers)
        assert user_answer.status_code == HTTPStatus.OK
        assert 'access_token' in user_answer.json()
        assert 'refresh_token' in user_answer.json()

    def test_user_take_auth_history(self, users):
        url = f'http://auth_api:8000/api/v1/auth/user/login'
        data = {
            'username': users[1].username,
            'password': '123',
        }
        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        tokens = requests.post(url, data=json_data, headers=headers).json()
        url = 'http://auth_api:8000/api/v1/auth/user/history'
        access = tokens['access_token']
        headers = {
            'Authorization': f'Bearer {access}',
            'Content-Type': 'application/json'
        }
        history = requests.get(url, headers=headers)
        assert history.status_code == HTTPStatus.OK
        assert len(history.json()) == 1
