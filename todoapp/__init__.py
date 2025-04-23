import os

from flask import Flask

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


    @app.route('/')
    def index():
        return 'ToDo задачник'

    return app
