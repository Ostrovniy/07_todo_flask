from datetime import datetime
from .db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean

# Ипользуем sqlite

class Users(db.Model): 
    """Пользователи сайта"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    url_photo: Mapped[str] = mapped_column(String(250), nullable=True)

    # Связь с задачами Users.tasks
    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

class Task(db.Model):
    """Задачи пользователей"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    # строка, представляющая дату добавления, формат YYYY-MM-DD HH:MM
    data_add: Mapped[str] = mapped_column(
        String(20), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M')
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Связь с пользователями Task.user
    user: Mapped["Users"] = relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"



