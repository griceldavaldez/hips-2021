
# app/__init__.py
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from werkzeug import utils
from config import app_config

login_manager = LoginManager()

def create_app(config_name):
    myInsLocation = os.path.dirname(__file__) + "/instance"
    app = Flask(__name__, 
    instance_path = myInsLocation,
    instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    login_manager.init_app(app)
    login_manager.login_message = "Debe acceder al sistema por el Login."
    login_manager.login_view = "auth.login"

    Bootstrap(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.route("/")
    def hello():
        return "Hello world!"

    return app