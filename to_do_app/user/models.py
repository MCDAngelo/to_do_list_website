import datetime as dt
from typing import List, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String

from to_do_app.database import db

if TYPE_CHECKING:
    from to_do_app.public.models import ToDoList
else:
    ToDoList = "ToDoList"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, unique=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, nullable=False, unique=False
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(150), nullable=True)
    lists: Mapped[List[ToDoList]] = relationship(back_populates="user")
