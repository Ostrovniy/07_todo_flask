import os
from flask import Flask
from todoapp.error import page_not_found, internal_server_error

#flask --app todoapp run --debug
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///todo.sqlite',  # или PostgreSQL если хочешь
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    from . import models  # 👈 ВАЖНО: импортируй модели до create_all / миграции
    db.init_app(app)

    # Регистрация ошибок сервера
    app.register_error_handler(404, page_not_found) #
    app.register_error_handler(500, internal_server_error)

    from . import auth
    app.register_blueprint(auth.auth_bp) #

    from . import tasks
    app.register_blueprint(tasks.tasks_bp)

        


    #@app.route('/')
    #def index():
        #return 'ToDo задачник'

    return app
