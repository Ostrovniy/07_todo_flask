import os
import functools
from functools import wraps
from flask import current_app
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from . import utils
from . import models
from . import db

# auth это имя блю принта
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Декторатор для проверки наличия авторизации
# Если не авторизован, нужно авторизацоваться
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            current_app.logger.info(f"Декоратор: нету авторизации, нужно авторизоваться")
            return redirect(url_for('auth.login'))  # или страница входа
        return view(**kwargs)
    return wrapped_view

# Если пользователь авторизован, лети на главную
def anonymous_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            current_app.logger.info(f"Декоратор: ты уже авторизовался, сюда нельзя")
            return redirect(url_for('tasks.index'))
        return view(**kwargs)
    return wrapped_view

# http://localhost:5000/auth/login
# Страница Входа на сайт: маршрут только для неаторизованных
@auth_bp.route('login', methods=["GET", "POST"])
@anonymous_required
def login():
    return render_template('login.html')

# КолБек для кнопки: "Войти через гугл" только для неавторизованных
@anonymous_required
@auth_bp.route('google', methods=["GET", "POST"])
def google():
    # Генерация уникального nonce
    nonce = os.urandom(16).hex()  
    
    # Сохраняем nonce в сессии
    session['nonce'] = nonce
    
    # Получаем базовый домен (например, через ngrok)
    #domain = utils.get_ngrok_url()
    # Публичный домен
    domain = 'https://07todoflask-production.up.railway.app'
    redirect_uri = f"{domain}/auth/google/callback"
    
    # Перенаправляем на страницу авторизации Google с передачей nonce
    return current_app.google.authorize_redirect(redirect_uri, nonce=nonce)

# Роутер обработки колбека от гугл
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
    
    # необходимые данные пользователя сохраняем в переменную
    username = user.email
    name =  user.name
    url_photo = user.picture
    current_app.logger.info(f"Данные от гугл: {username}, {name}, {url_photo}")

    # Поиск пользователя в бд
    user_mod = models.Users.query.filter_by(username = username).first()
    current_app.logger.info(f"Результат поиска пользователя в БД: {user_mod}")

    # Если пользователь есть в БД
    if user_mod:
        session['user'] = user_mod.id
        current_app.logger.info("Пользователь есть, добавить в сессию и перенаправть на главную страницу")
        return redirect(url_for('tasks.index'))
    # Если пользователя нету в бд
    else:
        current_app.logger.info("Пользователя нету")
        # Пользователя нету, нужно создать и добавить в сессию
        new_user = models.Users(
            username=username,
            name=name,
            url_photo=url_photo
        )
        db.db.session.add(new_user)
        db.db.session.commit()
        # new_user.id - будет доступный только после коммита
        session['user'] = new_user.id
        return redirect(url_for('tasks.index'))

# Выйти с аккаунта: Только для авторизованных
@auth_bp.route('logout', methods=["GET", "POST"])
@login_required
def logout():
    #current_app.logger.info("Выход, очистка сесси")
    session.clear()
    return redirect(url_for('auth.login'))

# Выполняеться перед каждый роутром
@auth_bp.before_app_request
def load_logged_in_user():
    # Получаем адишника пользователя с сесии
    user_id = session.get('user')

    # Добавляем пользователя в глобальную переменную g
    if user_id is None:
        #current_app.logger.info("load_logged_in_user: None")
        g.user = None
    else: 
        g.user = models.Users.query.filter_by(id = user_id).first()
        #current_app.logger.info(f"load_logged_in_user: {g.user}")

