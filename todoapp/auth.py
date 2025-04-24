import os
import functools

from flask import current_app
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import utils

# auth это имя блю принта
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# http://localhost:5000/auth/login
@auth_bp.route('login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

# http://127.0.0.1:5000/auth/google
@auth_bp.route('google', methods=["GET", "POST"])
def google():
    # Генерация уникального nonce
    nonce = os.urandom(16).hex()  # Генерация случайной строки для nonce
    
    # Сохраняем nonce в сессии
    session['nonce'] = nonce
    
    # Получаем базовый домен (например, через ngrok)
    domain = utils.get_ngrok_url()  # пример: https://d113-192-162-210-29.ngrok-free.app
    redirect_uri = f"{domain}/auth/google/callback"
    
    # Перенаправляем на страницу авторизации Google с передачей nonce
    return current_app.google.authorize_redirect(redirect_uri, nonce=nonce)

# Роутер обработки колбека от гугл
#https://d113-192-162-210-29.ngrok-free.app/auth/google/callback?provider=google
@auth_bp.route('google/callback', methods=["GET", "POST"])
def google_callback():
    # Получаем токен после авторизации
    token = current_app.google.authorize_access_token()
    
    # Извлекаем nonce из сессии
    nonce = session.get('nonce')
    if not nonce:
        # Если nonce отсутствует, обработайте ошибку
        return "Nonce is missing", 400

    # Проверка и парсинг ID токена с переданным nonce
    user = current_app.google.parse_id_token(token, nonce)
    
    # Логика работы с пользователем
    print(user)
    
    # Редирект на главную страницу
    return redirect(url_for('tasks.index'))
    
# http://localhost:5000/auth/logout
@auth_bp.route('logout', methods=[ "POST"])
def logout():
    return 'Выход с аккаунта'

