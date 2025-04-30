import os
from flask import Flask
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from todoapp.error import page_not_found, internal_server_error
from todoapp.utils import get_ngrok_url
import logging
from logging.handlers import RotatingFileHandler

#flask --app todoapp run --debug
def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    oauth = OAuth(app)

    #print(get_ngrok_url())

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///todo.sqlite',  # или PostgreSQL если хочешь
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_NAME = 'dev',
        GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID"),
        GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET"),
        GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration',
    )

    if test_config:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # штука называеться current_app
    app.google = google

    # ЛОГИРОВАНИЕ
    if app.debug:
        # Создаём директорию для логов, если нет
        os.makedirs("logs", exist_ok=True)

        file_handler = RotatingFileHandler("logs/app.log", maxBytes=10240, backupCount=3, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Приложение запущено")

    from . import db
    from . import models  # 👈 ВАЖНО: импортируй модели до create_all / миграции
    db.init_app(app)

    # Регистрация ошибок сервера
    app.register_error_handler(404, page_not_found) #
    app.register_error_handler(500, internal_server_error)

    from . import auth
    app.register_blueprint(auth.auth_bp) 

    from . import tasks
    app.register_blueprint(tasks.tasks_bp)

        


    #@app.route('/')
    #def index():
        #return 'ToDo задачник'

    return app
