from flask import Blueprint

crud = Blueprint('crud', __name__)

from . import views