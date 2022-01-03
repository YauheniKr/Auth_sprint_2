from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity, \
    decode_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from src.models.model_user import User, AuthHistory
from src.services.redis_service import RedisTokenStorage, InvalidTokenError


class UserRequest:

    def __init__(self, session):
        self.session = session

    def signup(self, create_data):
        create_data['password'] = generate_password_hash(create_data['password'], method='sha256')
        role = User(**create_data)
        try:
            self.session.add(role)
            self.session.commit()
        except IntegrityError:
            return None
        return {"msg": "role added"}

    def login(self):
        auth = request.json
        if not auth or not auth['username'] or not auth['password']:
            return make_response('username or password incorrect', 401)
        user = self.session.query(User).filter_by(username=auth['username']).first()
        self.session.commit()
        ipaddress = request.remote_addr
        user_agent = request.user_agent.string
        device = request.user_agent.platform
        history = AuthHistory(user_id = user.id, user_agent=user_agent, ip_address = ipaddress, device = device)
        if not user:
            return make_response('User not found', 401)
        if check_password_hash(user.password, auth['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            token = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            redis_service = RedisTokenStorage()
            refresh_token = decode_token(refresh_token)
            redis_service.add_token_to_database(refresh_token)
            self.session.add(history)
            self.session.commit()
            return token
        return make_response('Password incorrect', 401)

    @jwt_required()
    def logout(self):
        token = get_jwt()
        redis_service = RedisTokenStorage()
        redis_service.add_token_to_database(token)
        return jsonify(msg='Access token revoked')

    @jwt_required()
    def update(self, update_data):
        user_id = get_jwt()['sub']
        if not update_data:
            return make_response('User data incorrect', 400)
        password = update_data.get('password')
        if password:
            update_data['password'] = generate_password_hash(password, method='sha256')
        user = self.session.query(User).filter(User.id == user_id)
        self.session.commit()
        if not user:
            return make_response('User not found', 400)
        user.update(update_data)
        self.session.commit()
        return make_response('User data updated', 200)



class TokenRequest:

    @jwt_required(refresh=True)
    def refresh_token(self):
        token = get_jwt()
        identity = get_jwt_identity()
        redis_service = RedisTokenStorage()
        try:
            redis_service.jti_refresh_token(token)
        except InvalidTokenError:
            return make_response('Token is absent or incorrect', 401,
                                 {'Authentication': 'Token is absent or incorrect'})
        else:
            access_token = create_access_token(identity)
            refresh_token = create_refresh_token(identity)
            token = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            redis_service = RedisTokenStorage()
            refresh_token = decode_token(refresh_token)
            redis_service.add_token_to_database(refresh_token)
        return token
