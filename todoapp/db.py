from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_app(app):
    db.init_app(app)

    @app.cli.command("init-db")
    def init_db_command():
        """Создаёт таблицы в базе данных."""
        with app.app_context():
            db.create_all()
        print("База данных и таблицы созданы.")
