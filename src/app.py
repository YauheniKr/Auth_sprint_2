from flasgger import Swagger
from flask import Flask, request, make_response
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.api.oauth_api import oauth_blueprint
from src.api.role_api import roles_blueprint, roles_status_blueprint
from src.api.user_api import token_blueprint, user_blueprint
from src.commands import usersbp
from src.core.config import settings

app = Flask(__name__)
swagger = Swagger(app)
app.config['JWT_SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = settings.ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = settings.REFRESH_EXPIRES
app.config["SECRET_KEY"] = settings.SECRET_KEY

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
app.register_blueprint(oauth_blueprint)

app.config['OAUTH_CREDENTIALS'] = {
    'yandex': {
        'id': settings.YANDEX_ID,
        'secret': settings.YANDEX_PASWORD
    },
}

from jaeger_client import Config
from flask_opentracing import FlaskTracer


#@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return make_response('X-Request-Id not found', 404)


config_data = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'local_agent': {
        'reporting_host': '192.168.88.131',
        'reporting_port': '6831',
    },
    'logging': True,
}


def _setup_jaeger():
    config = Config(config=config_data, service_name="movies-api", validate=True, )
    return config.initialize_tracer()


tracer = FlaskTracer(_setup_jaeger, app=app)

if __name__ == '__main__':
    app.run()
