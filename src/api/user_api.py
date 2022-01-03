from http import HTTPStatus

from flask import request
from flask_restful import Resource

from src.db.global_init import create_session
from src.services.user import UserRequest, TokenRequest


class UserCreate(Resource):

    def post(self):
        session = create_session()
        json_data = request.get_json(force=True)
        user = UserRequest(session)
        user = user.signup(json_data)
        if not user:
            return f'Пользователь с данными параметрами уже существует', HTTPStatus.CONFLICT
        session.close()
        return {'msg': 'Пользователь создан'}


class UserLogin(Resource):

    def post(self):
        session = create_session()
        user = UserRequest(session)
        user = user.login()
        session.close()
        return user


class UserLogout(Resource):
    def get(self):
        session = create_session()
        user = UserRequest(session)
        user = user.logout()
        session.close()
        return user


class UserUpdate(Resource):
    def patch(self):
        json_data = request.get_json(force=True)
        session = create_session()
        user = UserRequest(session)
        user = user.update(json_data)
        return user


class TokenRefresh(Resource):

    def post(self):
        token = TokenRequest()
        token = token.refresh_token()
        return token
