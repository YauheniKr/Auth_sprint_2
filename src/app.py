from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

import datetime

from src.api.role_api import RoleCreate, RoleGetUpdateDelete, RolesGet, RoleUserCreateDelete, CheckUserRole
from src.api.user_api import UserCreate, UserLogin, UserLogout, TokenRefresh, UserUpdate
from src.core.config import settings

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = settings.SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.REFRESH_EXPIRES

api = Api(app)
jwt = JWTManager(app)
api.add_resource(RoleGetUpdateDelete, '/api/v1/auth/role/<string:role_id>')
api.add_resource(RoleCreate, '/api/v1/auth/role/')
api.add_resource(RolesGet, '/api/v1/auth/roles/')
api.add_resource(RoleUserCreateDelete, '/api/v1/auth/role/user/')
api.add_resource(CheckUserRole, '/api/v1/auth/role/user/status')
api.add_resource(UserCreate, '/api/v1/auth/user/signup')
api.add_resource(UserLogin, '/api/v1/auth/user/login')
api.add_resource(UserLogout, '/api/v1/auth/user/logout')
api.add_resource(TokenRefresh, '/api/v1/auth/token/refresh')
api.add_resource(UserUpdate, '/api/v1/auth/user/me')

if __name__ == '__main__':
    app.run()
