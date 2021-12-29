from http import HTTPStatus

from flask import request
from flask_pydantic import validate
from flask_restful import Resource

from src.db.global_init import create_session
from src.models.pydantic_models import RoleModel, RoleUserModel
from src.services.role import RoleRequest, RolesRequest, RoleUserRequest


class RoleGetUpdateDelete(Resource):
    """Single object resource
    ---
    get:
      tags:
        - api
      summary: Get a user
      description: Get a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchema
        404:
          description: user does not exists
    put:
      tags:
        - api
      summary: Update a user
      description: Update a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user updated
                  user: UserSchema
        404:
          description: user does not exists
    delete:
      tags:
        - api
      summary: Delete a user
      description: Delete a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user deleted
        404:
          description: user does not exists
    """

    # method_decorators = [jwt_required()]
    @validate()
    def get(self, role_id):
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.get_role()
        session.close()
        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        return RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight)

    @validate()
    def patch(self, role_id):
        json_data = request.get_json(force=True)
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.update_role(json_data)
        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        session.close()
        return RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight)

    @validate()
    def delete(self, role_id):
        session = create_session()
        role = RoleRequest(role_id, session)
        role = role.delete_role()
        if not role:
            return f'Не найдена роль с id {role_id}', HTTPStatus.NOT_FOUND
        session.close()
        return {"msg": "Роль удалена"}


class RoleCreate(Resource):

    def post(self):
        session = create_session()
        json_data = request.get_json(force=True)
        role = RolesRequest(session)
        role = role.create_role(json_data)
        if not role:
            return f'Роль с данными параметрами уже существует', HTTPStatus.CONFLICT
        session.close()
        return {'msg': 'Роль создана'}


class RolesGet(Resource):

    @validate(response_many=True)
    def get(self) -> list[RoleModel]:
        session = create_session()
        roles = RolesRequest(session)
        roles = roles.get_roles()
        roles = [RoleModel(id=role.id, role_name=role.role_name, role_weight=role.role_weight) for role in roles]
        return roles


class RoleUserCreateDelete(Resource):

    def post(self):
        session = create_session()
        json_data = request.get_json(force=True)
        user_role = RoleUserRequest(session)
        user_role = user_role.user_add_role(json_data)
        if not user_role:
            return f'User с данной ролью уже существует', HTTPStatus.CONFLICT
        elif 'DETAIL' in user_role:
            return user_role, HTTPStatus.CONFLICT
        return {'msg': 'Роль добавлена'}

    def delete(self):
        session = create_session()
        json_data = request.get_json(force=True)
        user_role = RoleUserRequest(session)
        user_role = user_role.user_delete_role(json_data)
        session.close()
        if not user_role:
            return f'User не существует', HTTPStatus.NOT_FOUND
        return {"msg": "role deleted"}


class CheckUserRole(Resource):

    @validate()
    def get(self):
        session = create_session()
        json_data = request.get_json(force=True)
        user_role_status = RoleUserRequest(session)
        user_role_status = user_role_status.get_user_status(json_data)
        return RoleUserModel(role_name=user_role_status['role_name'], role_weight=user_role_status['role_weight'])
