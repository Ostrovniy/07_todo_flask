import sqlite3
from datetime import datetime

import click
from flask import current_app, g
# g — временное хранилище данных на время запроса (например, БД)


# Получает подключение к базе данных.
# Если подключения ещё нет, создаёт его и сохраняет в g (для повторного использования в рамках одного запроса).
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

# Если соидинения есть в g, то оно будет закрыто
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # Получаем подключение к базе данных
    db = get_db()

    # Открываем SQL-файл и выполняем все команды (например, создание таблиц)
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# это команда для терминала: flask init-db
@click.command('init-db')
def init_db_command():
    """Очищает старые данные и создаёт новые таблицы."""
    init_db()
    click.echo('Initialized the database.')

# Регистрируем конвертер: если в БД есть поле типа "timestamp",
# оно автоматически превращается в объект datetime при чтении
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # сообщает Flask вызвать эту функцию при очистке после возврата ответа.
    app.teardown_appcontext(close_db)
    # добавляет новую команду, которая может быть вызвана с помощью команды flask.
    app.cli.add_command(init_db_command)
