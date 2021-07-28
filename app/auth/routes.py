from flask import (render_template, redirect, url_for,
                   request, current_app)
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from Configuraciones import utils

from app import login_manager

from . import auth_bp
from .forms import LoginForm
from Configuraciones.modelos import Usuario


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = utils.obtenerUsuario(form.login.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(login):
    return utils.obtenerUsuario(login)
