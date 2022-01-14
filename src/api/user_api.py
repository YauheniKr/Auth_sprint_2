from http import HTTPStatus

from flask import request
from flask_pydantic import validate
from flask_restful import Resource

from src.db.global_init import create_session
from src.models.pydantic_models import AuthHistoryModel, AuthHistoryBase
from src.services.user import AuthHistoryRecord, TokenRequest, UserRequest
from src.services.utils import get_paginated_list


class UserCreate(Resource):

    def post(self):
        """
        Этот метод создает пользователя.
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            schema:
              id: User
              properties:
                username:
                  type: string
                  required: true
                  description: имя пользователя
                password:
                  type: string
                  required: true
                  description: пароль пользователя
                email:
                  type: string
                  required: true
                  description: email пользователя

        responses:
          200:
            description: Пользователь создан
          409:
            description: Пользователь с данными параметрами уже существует
        """
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
        """
        Вход пользователя в аккаунт. В обмен на ввод пары login/password мы получаем 2 токена
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            schema:
              properties:
                username:
                  type: string
                  required: true
                  description: имя пользователя
                password:
                  type: string
                  required: true
                  description: пароль пользователя

        responses:
          200:
            description: Succesfully logged
            schema:
              properties:
                access token:
                  type: string
                  description: access token
                refresh token:
                  type: string
                  description: refresh token
          404:
            description: User not found
          401:
            description: Пароль некорректен
        """
        session = create_session()
        user = UserRequest(session)
        user = user.login()
        session.close()
        return user


class UserLogout(Resource):
    def get(self):
        """
        Выход пользователя из аккаунта.
        ---
        tags:
          - User
        parameters:
          - name: body
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа

        responses:
          200:
            description: Succesfully logged out
        """
        session = create_session()
        user = UserRequest(session)
        user = user.logout()
        session.close()
        return user


class UserUpdate(Resource):
    def patch(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - User
        parameters:
          - name: Authorization
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа. Добавляем Bearer в начало токена при тестировании
          - name: body
            in: body
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: имя пользователя
                password:
                  type: string
                  description: пароль пользователя
                email:
                  type: string
                  description: email пользователя
        responses:
          200:
            description: User data updated
          400:
            description: User data incorrect
          404:
            description: User not found
        """
        json_data = request.get_json(force=True)
        session = create_session()
        user = UserRequest(session)
        user = user.update(json_data)
        return user


class GetUserAuthHistory(Resource):

    @validate(response_by_alias=True)
    def get(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - AuthHistory
        parameters:
          - name: page
            in: query
            schema:
              properties:
                page:
                  type: integer
                  description: Номер страницы
                  default: 1
          - name: limit
            in: query
            schema:
              properties:
                page:
                  type: integer
                  description: Количество записей на странице
                  default: 5
          - name: Authorization
            in: header
            schema:
              properties:
                access_token:
                  type: string
                  required: true
                  description: токен доступа. Добавляем Bearer в начало токена при тестировании
        responses:
          200:
            description: list of AuthHistory items
            schema:
              id: AuthHistoryModel
              properties:
                id:
                  type: string
                  description: идентификатор записи. Формат uuid4
                timestamp:
                  type: string
                  description:  дата входа в аккаунт
                user_agent:
                  type: string
                  description: описание программы с которого входили в аккаунт
                ip_address:
                  type: string
                  description: ip address устройства с которого входили в аккаунт
                device:
                  type: string
                  description: описание описание устройства с которго входили в аккаунт
        """
        session = create_session()
        auth_history = AuthHistoryRecord(session)
        auth_history = auth_history.get_auth_record()
        session.close()
        history = [AuthHistoryBase(id=record.id, timestamp=record.timestamp, user_agent=record.user_agent,
                                   ipaddress=record.ip_address, device=record.device)
                   for record in auth_history]

        auth_record_out = get_paginated_list(
            history,
            '/api/v1/auth/user/history',
            page=request.args.get('page', 1),
            limit=request.args.get('limit', 5)
        )
        out = AuthHistoryModel(**auth_record_out)
        return out


class TokenRefresh(Resource):

    def post(self):
        """
        Обновление информации о пользователе
        ---
        tags:
          - User
        parameters:
          - name: Authorization
            in: header
            schema:
              properties:
                refresh_token:
                  type: string
                  required: true
                  description: токен обновления. Добавляем Bearer в начало токена при тестировании
        responses:
          200:
            description: Tokens updated
          401:
            description: Token is absent or incorrect
        """
        token = TokenRequest()
        token = token.refresh_token()
        return token
