from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.api.role_api import roles_blueprint, roles_status_blueprint
from src.api.user_api import token_blueprint, user_blueprint
from src.commands import usersbp
from src.core.config import settings

app = Flask(__name__)
swagger = Swagger(app)
app.config['JWT_SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.REFRESH_EXPIRES

jwt = JWTManager(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['200 per day', '50 per hour']
)
limiter.limit('10 per second')(roles_status_blueprint)

app.register_blueprint(usersbp)
app.register_blueprint(roles_blueprint)
app.register_blueprint(roles_status_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(token_blueprint)

if __name__ == '__main__':
    app.run()
