import os

from flask import Flask

#flask --app todoapp run --debug
def create_app(test_config=None):
    # create and configure the app
    # __name__ имя текущего модуля, нужно для настройки путей
    app = Flask(__name__, instance_relative_config=True)

    # Указание конфигурации приложения по умолчанию
    # SECRET_KEY - какой то ключ, при развертывании нужно указать рандомную строку
    # DATABASE - Путь к БД / app.instance_path - путь к папке где будет БД по умолчанию
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Здесь пока что не понятно, дает возможность задать конфигурацию по разному
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # Проверка что папка для БД находиться в проекте
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return 'ToDo задачник'
    
    # Иницыализация БД
    from . import db
    db.init_app(app)

    # Блю принт, авторизации (Регистрация)
    #from . import auth
    #app.register_blueprint(auth.bp)

    # Блю принт для блога
    #from . import blog
    #app.register_blueprint(blog.bp)
    # это сделано что бы можно было ссылаться на страницу blog.index
    #app.add_url_rule('/', endpoint='index')

    return app