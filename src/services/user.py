from http import HTTPStatus
from flask import make_response, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                decode_token, get_jwt, get_jwt_identity,
                                jwt_required)
from sqlalchemy import desc, or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from src.models.model_user import AuthHistory, User, SocialAccount
from src.services.redis_service import InvalidTokenError, RedisTokenStorage
from src.services.utils import generate_tokens


class UserRequest:

    def __init__(self, session):
        self.session = session

    def signup(self, create_data):
        create_data['password'] = generate_password_hash(create_data['password'], method='sha256')
        user = User(**create_data)
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            return None
        return make_response({'msg': 'user created'}, 200)

    def login(self):
        auth = request.json
        is_admin = False
        if not auth or not auth['username'] or not auth['password']:
            return make_response('username or password absent', 401)
        user = self.session.query(User).filter_by(username=auth['username']).first()
        self.session.commit()
        if not user:
            return make_response('User not found', 404)
        if user.role and user.role[0].role_name == 'superuser':
            is_admin = True
        if check_password_hash(user.password, auth['password']):
            token = generate_tokens(user.id, is_admin)
            ipaddress = request.remote_addr
            user_agent = request.user_agent.string
            device = request.user_agent.platform
            history = AuthHistory(user_id=user.id, user_agent=user_agent, ip_address=ipaddress, device=device)
            self.session.add(history)
            self.session.commit()
            return token
        return make_response('Password incorrect', 401)

    @jwt_required()
    def logout(self):
        token = get_jwt()
        redis_service = RedisTokenStorage()
        redis_service.add_token_to_database(token)
        return make_response('Token revoked', 200)

    @jwt_required()
    def update(self, update_data):
        user_id = get_jwt()['sub']
        if not update_data:
            return make_response('User data incorrect', 400)
        user = self.session.query(User).filter(User.id == user_id)
        self.session.commit()
        if not user:
            return make_response('User not found', 404)
        password = update_data.get('password')
        if password:
            update_data['password'] = generate_password_hash(password, method='sha256')
        user.update(update_data)
        self.session.commit()
        return make_response('User data updated', 200)

    def auth_login(self, user_data):
        user = self.session.query(User).filter(
            or_(User.username == user_data['login'], User.email == user_data['default_email'])).first()
        social_user = self.session.query(SocialAccount).filter(SocialAccount.social_id == user_data['id']).first()
        if not user:
            user = User(username=user_data['login'], email=user_data['default_email'])
            self.session.add(user)
            self.session.commit()
        if not social_user:
            self.session.add(SocialAccount(social_id=user_data['id'], social_name=user_data['login'], user_id=user.id))
            self.session.commit()
        tokens = generate_tokens(user.id)
        return tokens


class TokenRequest:

    @jwt_required(refresh=True)
    def refresh_token(self):
        is_admin = False
        token = get_jwt()
        identity = get_jwt_identity()
        redis_service = RedisTokenStorage()
        try:
            redis_service.jti_refresh_token(token)
        except InvalidTokenError:
            return make_response('Token is absent or incorrect', 401,
                                 {'Authentication': 'Token is absent or incorrect'})
        else:
            if token.get('is_administrator'):
                is_admin = True
            token = generate_tokens(identity, is_admin)
        return token


class AuthHistoryRecord:

    def __init__(self, session):
        self.session = session

    @jwt_required()
    def get_auth_record(self):
        user_id = get_jwt()['sub']
        auth_record = self.session.query(AuthHistory).filter_by(user_id=user_id).order_by(desc(AuthHistory.timestamp))
        self.session.commit()
        return auth_record
