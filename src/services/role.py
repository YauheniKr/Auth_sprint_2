from flask import make_response
from sqlalchemy.exc import IntegrityError

from src.models.model_role import Role, RoleUser
from src.models.model_user import User
from src.services.utils import admin_required


class RoleRequest:

    def __init__(self, role_id, session):
        self.role_id = role_id
        self.session = session

    def get_role(self):
        role = self.session.query(Role).get(self.role_id)
        if not role:
            return None
        return role

    def update_role(self, updated_data):
        role = self.session.query(Role).filter(Role.id == self.role_id)
        role_status = role.update(updated_data)
        self.session.commit()
        if role_status == 0:
            return None
        role = self.session.query(Role).filter_by(id=self.role_id).first()
        return role

    def delete_role(self):
        role = self.session.query(Role).filter(Role.id == self.role_id)
        role_status = role.delete()
        self.session.commit()
        if role_status == 0:
            return None
        return {"msg": "role deleted"}


class RolesRequest:

    def __init__(self, session):
        self.session = session

    def create_role(self, create_data):

        if create_data['role_name'] == 'superuser':
            return {"msg": "superuser"}
        role = Role(**create_data)
        try:
            self.session.add(role)
            self.session.commit()
        except IntegrityError:
            return None
        return {"msg": "role added"}

    def get_roles(self):
        roles = self.session.query(Role).all()
        return roles


class RoleUserRequest:

    def __init__(self, session):
        self.session = session

    def get_user_status(self, user_data):
        user_id = user_data.get('user_id')
        if not user_id:
            user_status = {
                'role_weight': 0,
                'role_name': 'anonymous'
            }
            return user_status
        user = self.session.query(User).filter_by(id=user_id).first()
        self.session.commit()
        if not user:
            user_role_weight = 0
            user_role_name = 'anonymous'
        elif user and not user.role:
            user_role_weight = 1
            user_role_name = 'user'
        else:
            user_role_weight = user.role[0].role_weight
            user_role_name = user.role[0].role_name
        user_status = {
            'role_name': user_role_name,
            'role_weight': user_role_weight,
        }
        return user_status

    @admin_required()
    def user_add_role(self, create_data):
        role_user_exists = self.session.query(RoleUser).filter_by(**create_data).first()
        self.session.commit()
        if role_user_exists:
            return None
        role_user = RoleUser(**create_data)
        try:
            self.session.add(role_user)
            self.session.commit()
            return make_response('created successfully', 200)
        except IntegrityError as error:
            return error.orig.pgerror.split('\n')[1]

    @admin_required()
    def user_delete_role(self, delete_data):
        user_role = self.session.query(RoleUser).filter_by(**delete_data).first()
        self.session.commit()
        if not user_role:
            return None
        self.session.delete(user_role)
        self.session.commit()
        return make_response('role deleted', 200)
