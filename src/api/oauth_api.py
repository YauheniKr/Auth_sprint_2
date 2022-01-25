from http import HTTPStatus

from authlib.integrations.flask_client import OAuth
from flask import current_app as app, url_for, Blueprint, make_response
from flask_restful import Resource, Api

from src.core.config import settings
from src.db.global_init import create_session
from src.services.user import UserRequest

oauth = OAuth(app)

oauth_blueprint = Blueprint('oauth', __name__)
oauth_api = Api(oauth_blueprint, prefix='/api/v1/auth')

access_data = {
    'grant_type': 'authorization_code',
    'client_id': settings.YANDEX_ID,
    'client_secret': settings.YANDEX_PASSWORD,
}

oauth.register('yandex', client_id=settings.YANDEX_ID, client_secret=settings.YANDEX_PASSWORD,
               authorize_url='https://oauth.yandex.ru/authorize', access_token_url='https://oauth.yandex.ru/token',
               access_token_params=access_data, userinfo_endpoint='https://login.yandex.ru/info',)


class YandexLogin(Resource):

    def get(self, social_name: str):
        client = oauth.create_client(social_name)
        if not client:
            return make_response({'msg': f'{client} not found'}, HTTPStatus.NOT_FOUND)
        redirect_url = url_for(
            "oauth.oauthauthorization", social_name=social_name, _external=True,
        )
        return client.authorize_redirect(redirect_url)


class OauthAuthorization(Resource):

    def get(self, social_name: str):
        client = oauth.create_client(social_name)
        if not client:
            return make_response({'msg': f'{client} not found'}, HTTPStatus.NOT_FOUND)
        token = client.authorize_access_token()
        user_info = oauth.yandex.userinfo()
        session = create_session()
        user = UserRequest(session)
        user = user.auth_login(user_info)

        # oauth_service = OauthService(
        #    social_name,
        #    user_info["sub"],
        #    user_info["name"],
        #    user_info["email"],
        # )
        # print(user_info)
        # try:
        #    access_token, refresh_token = oauth_service.login(request)
        # except OauthServiceError:
        #    raise exceptions.Unauthorized()
        #
        # return jsonify(access_token=access_token, refresh_token=refresh_token)


oauth_api.add_resource(YandexLogin, '/oauth/login/<string:social_name>')
oauth_api.add_resource(OauthAuthorization, '/oauth/callback/<string:social_name>')
