from flask import Blueprint
from src.views.auth import Auth
from src.views.base import home_controller
from flask_login import  login_required, logout_user


auth_router = Blueprint('auth', __name__, url_prefix='/auth')


@auth_router.route('/login', methods=['GET', 'POST'])
def login():
    return Auth.login()


@auth_router.route('/register', methods=['GET', 'POST'])
def register():
    return Auth.register()


@auth_router.route('/logout')
@login_required
def logout():
    logout_user()
    return home_controller()