from flask import render_template
import flask
from flask_login import login_required

from . import home
import main


@home.route('/')
@login_required
def homepage():
    return render_template('home/index.html', title="HIPS")

@home.route('/scan')
@login_required
def iniciar_escaneo():
    flask('Se inició el escaneo...')
    main.main()
    flask('Escaneo finalizado.')
    return render_template('home/index.html', title="HIPS")