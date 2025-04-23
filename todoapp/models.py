from .db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    test: Mapped[str] = mapped_column(String(255))
