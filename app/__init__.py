
# app/__init__.py
import os
from flask import Flask
from werkzeug import utils
from config import app_config

def create_app(config_name):
    myInsLocation = os.path.dirname(__file__) + "/instance"
    app = Flask(__name__, 
    instance_path = myInsLocation,
    instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route("/")
    def hello():
        return "Hello world!"

    return app