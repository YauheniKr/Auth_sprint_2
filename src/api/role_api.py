import uuid
from http import HTTPStatus
from typing import Union

from flask import request, Blueprint
from flask_pydantic import validate
from flask_restful import Resource, Api

from src.db.global_init import create_session
from src.models.pydantic_models import RoleModel, RoleUserModel
from src.services.role import RoleRequest, RolesRequest, RoleUserRequest

roles_blueprint = Blueprint('roles', __name__)
roles_status_blueprint = Blueprint('roles_status', __name__)
api = Api(roles_blueprint, prefix='/api/v1/auth')
api_status = Api(roles_status_blueprint, prefix='/api/v1/auth')


class RoleGetUpdateDelete(Resource):

    @validate()
    def get(self, role_id: uuid.UUID) -> Union[RoleModel, tuple]:
        """
        Этот метод возвращает информацию о роли по ее role_id
        ---
        tags:
          - Role
        parameters:
          - in: path
            name: role_id
            type: string
            required: true
        responses:
          200:
            description: A single role item
            schema:
              id: RoleModel
              properties:
                id:
                  type: string
                  description: идентификатор роли. Формат uuid4
                role_weight:
                  type: integer
                  description:  вес роли. Используется для определения возможности получения запрашиваемой информации
                role_name:
                  type: string
                  description: имя роли
                description:
                  type: string
                  description: описание роли
          404:
            description: Роль с заданным id не найдена
        """
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.get_role()
        session.close()
        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        return RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight,
                         description=role.description)

    @validate()
    def patch(self, role_id: uuid.UUID) -> Union[RoleModel, tuple]:
        """
        Этот метод обновляет информацию о роли по ее role_id и возвращет обновленную информацию
        ---
        tags:
          - Role
        parameters:
          - in: path
            name: role_id
            type: string
            required: true
          - in: body
            name: body
            schema:
              properties:
                role_name:
                  type: string
                  description: имя роли
                role_weight:
                  type: integer
                  description: вес роли
                description:
                  type: string
                  description: описание роли
        responses:
          200:
            description: A single role item
            schema:
              id: RoleModel
              properties:
                id:
                  type: string
                  description: идентификатор роли. Формат uuid4
                role_weight:
                  type: integer
                  description:  вес роли. Используется для определения возможности получения запрашиваемой информации
                role_name:
                  type: string
                  description: имя роли
                description:
                  type: string
                  description: описание роли
          404:
            description: Роль с заданным id не найдена
        """
        json_data = request.get_json(force=True)
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.update_role(json_data)

        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        session.close()
        return RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight,
                         description=role.description)

    @validate()
    def delete(self, role_id: uuid.UUID) -> Union[dict[str], tuple]:
        """
        Этот метод удаляет информацию о роли по ее role_id
        ---
        tags:
          - Role
        parameters:
          - in: path
            name: role_id
            type: string
            required: true
        responses:
          200:
            description: Сообщение об успешном удалении роли
          404:
            description: Роль с заданным id не найдена
        """
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.delete_role()
        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        session.close()
        return {"msg": "Роль удалена"}


class RoleCreate(Resource):

    def post(self) -> Union[dict[str], tuple]:
        """
        Этот метоl создает роль по предоставленной информации в теле запроса
        ---
        tags:
          - Role
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                role_name:
                  type: string
                  required: true
                  description: имя роли
                role_weight:
                  type: integer
                  required: true
                  description: вес роли
                description:
                  type: string
                  description: описание роли
        responses:
          200:
            description: Роль создана
          409:
            description: Роль с данными параметрами уже существует
        """
        session = create_session()
        json_data = request.get_json(force=True)
        role = RolesRequest(session)
        role = role.create_role(json_data)
        if not role:
            return f'Роль с данными параметрами уже существует', HTTPStatus.CONFLICT
        elif role['msg'] == 'superuser':
            return f'Роль superuser можно создать только консольной командой', HTTPStatus.CONFLICT
        session.close()
        return {'msg': 'Роль создана'}


class RolesGet(Resource):

    @validate(response_many=True)
    def get(self) -> list[RoleModel]:
        """
        Этот метод возвращает список существующих ролей
        ---
        tags:
          - Role
        responses:
          200:
            description: Список ролей
            schema:
              id: RoleModel
              properties:
                id:
                  type: string
                  description: идентификатор роли. Формат uuid4
                role_weight:
                  type: integer
                  description:  вес роли. Используется для определения возможности получения запрашиваемой информации
                role_name:
                  type: string
                  description: имя роли
                description:
                  type: string
                  description: описание роли
        """
        session = create_session()
        roles = RolesRequest(session)
        roles = roles.get_roles()
        roles = [RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight,
                           description=role.description) for role in roles]
        return roles


class RoleUserCreateDelete(Resource):

    def post(self) -> Union[dict[str], tuple]:
        """
        Этот метод назначает роль пользователю. Предварительно и пользователь и роль должны быть созданы в БД
        ---
        tags:
          - RoleUser
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
            required: true
            schema:
              id: RoleUser
              properties:
                role_id:
                  type: string
                  required: true
                  description: идентификатор роли
                user_id:
                  type: integer
                  required: true
                  description: идентификатор пользователя

        responses:
          200:
            description: Роль добавлена
          403:
            description: Пользователь не корректен
          409:
            description: Пользователь с данной ролью уже существует
        """
        session = create_session()
        json_data = request.get_json(force=True)
        user_role = RoleUserRequest(session)
        user_role = user_role.user_add_role(json_data)
        if not user_role:
            return f'User с данной ролью уже существует', HTTPStatus.CONFLICT
        elif user_role.status_code == 403:
            return user_role
        return user_role

    def delete(self) -> Union[dict[str], tuple]:
        """
        Этот метод удаяляет роль у пользователя.
        ---
        tags:
          - RoleUser
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: RoleUser
              properties:
                user_id:
                  type: string
                  required: true
                  description: идентификатор пользователя

        responses:
          200:
            description: Роль удалена
          403:
            description: Пользователь не корректен
          409:
            description: Пользователь не существует
        """
        session = create_session()
        json_data = request.get_json(force=True)
        user_role = RoleUserRequest(session)
        user_role = user_role.user_delete_role(json_data)
        session.close()
        if not user_role:
            return f'User не существует', HTTPStatus.NOT_FOUND
        return user_role


class CheckUserRole(Resource):

    @validate()
    def get(self) -> RoleUserModel:
        """
        Этот метод возвращает статус пользователя
        ---
        tags:
          - RoleUser
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                user_id:
                  type: string
                  required: true
                  description: идентификатор пользователя
        responses:
          200:
            description: Роль для данного пользователя по его user_id
            schema:
              properties:
                role_weight:
                  type: integer
                  description:  вес роли. Используется для определения возможности получения запрашиваемой информации
                role_name:
                  type: string
                  description: имя роли
        """
        session = create_session()
        json_data = request.get_json(force=True)
        user_role_status = RoleUserRequest(session)
        user_role_status = user_role_status.get_user_status(json_data)
        return RoleUserModel(role_name=user_role_status['role_name'], role_weight=user_role_status['role_weight'])


api.add_resource(RoleGetUpdateDelete, '/role/<string:role_id>/')
api.add_resource(RoleCreate, '/role/')
api.add_resource(RolesGet, '/roles/')
api.add_resource(RoleUserCreateDelete, '/role/user/')
api_status.add_resource(CheckUserRole, '/role/user/status/')
