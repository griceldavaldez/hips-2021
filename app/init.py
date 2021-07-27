
from flask import Flask, render_template, redirect, url_for,request, flash, Blueprint
from flask_login import current_user, login_user, logout_user, LoginManager
from werkzeug.urls import url_parse

from auth.forms import SignupForm, LoginForm

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

    return app


def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime


app = create_app()


@app.route("/")
def hello():
    return "Hello world!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

