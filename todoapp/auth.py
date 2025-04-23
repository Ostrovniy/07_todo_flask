import functools
# Роутеры для работы с авторизацией
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# auth это имя блю принта
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# http://localhost:5000/auth/login
@auth_bp.route('login', methods=('GET', 'POST'))
def login():
    return 'Страница регистрации авторизации'

# http://localhost:5000/auth/logout
@auth_bp.route('logout', methods=('GET', 'POST'))
def logout():
    return 'Выход с аккаунта'

# Страницы для авторизации
# Страница для выхода с авторизации