
from flask import Flask, render_template, redirect, url_for,request, flash, Blueprint
from flask_login import current_user, login_user, logout_user, LoginManager
from werkzeug.urls import url_parse
from Configuraciones import utils
import os

from app.auth.forms import LoginForm

from app.common.filters import format_datetime

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Registro de los filtros
    register_filters(app)

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)
    
    app.config["SECRET_KEY"] = os.urandom(32)

    return app


def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime


app = create_app()


@app.route("/")
def hello():
    return "Hello world!"

