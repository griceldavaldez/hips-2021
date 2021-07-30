from flask import render_template, flash
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
    flash('Se inició el escaneo...')
    main.main()
    flash('Escaneo finalizado.')
    return render_template('home/index.html', title="HIPS")