from flask import Flask

from src.services.role import role_route

app = Flask(__name__)
app.register_blueprint(role_route)

if __name__ == '__main__':
    app.run()
