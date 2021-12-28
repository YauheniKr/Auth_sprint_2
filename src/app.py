from flask import Flask
from flask_restful import Api

from src.api.role_api import RoleCreate, RoleGetUpdateDelete, RolesGet, RoleUserCreateDelete, CheckUserRole

app = Flask(__name__)
api = Api(app)
api.add_resource(RoleGetUpdateDelete, '/api/v1/auth/role/<string:role_id>')
api.add_resource(RoleCreate, '/api/v1/auth/role/')
api.add_resource(RolesGet, '/api/v1/auth/roles/')
api.add_resource(RoleUserCreateDelete, '/api/v1/auth/role/user/')
api.add_resource(CheckUserRole, '/api/v1/auth/role/user/status')

if __name__ == '__main__':
    app.run()
