

from flask import abort, render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from . import public_bp

@public_bp.route("/")
@login_required
def index():
    return render_template("public/index.html")
