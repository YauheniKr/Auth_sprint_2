import click
from flask import Blueprint
from werkzeug.security import generate_password_hash

from src.db.global_init import create_session
from src.models.model_role import Role, RoleUser
from src.models.model_user import User

usersbp = Blueprint('superuser', __name__)


@usersbp.cli.command('create')
@click.argument('username')
@click.argument('password')
@click.argument('email')
def create_superuser(username, password, email):
    session = create_session()
    user = session.query(User).filter(username == username, email == email).all()
    session.commit()
    if not user:
        password = generate_password_hash(password)
        user = User(username=username, password=password, email=email)
        session.add(user)
        session.commit()
        role_id = create_superuser_role()
        roleuser = RoleUser(user_id=user.id, role_id=role_id)
        session.add(roleuser)
        session.commit()
        session.close()
        print('user successfully created')
    else:
        print('User with this parameters already exists')


def create_superuser_role():
    session = create_session()
    role = session.query(Role).filter_by(role_name='superuser').first()
    if not role:
        role = Role(role_name='superuser', role_weight=5, description='superuser role')
        session.add(role)
        session.commit()
    return role.id
