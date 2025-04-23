from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()  # создаем экземпляр

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)  # <-- добавь это 
