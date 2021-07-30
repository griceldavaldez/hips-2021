# app/auth/views.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import utils

from app import login_manager

from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = utils.obtenerUsuario(form.login.data)
        if user is not None: 
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('home.homepage')
                return redirect(next_page)
            else:
                flash('Credenciales incorrectas.', 'error')
        else:
            flash('Usuario no encontrado.', 'error')
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión terminada correctamente.')
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return utils.obtenerUsuarioPorId(int(user_id))