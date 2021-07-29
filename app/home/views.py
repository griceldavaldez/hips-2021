from flask import render_template
from flask_login import login_required

from . import home


@home.route('/')
@login_required
def homepage():
    return render_template('home/index.html', title="HIPS")