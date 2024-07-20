import datetime as dt
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String

from to_do_app.database import db

if TYPE_CHECKING:
    from to_do_app.user.models import User
else:
    User = "User"


class ToDoList(db.Model):
    __tablename__ = "lists"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    items: Mapped[List["ToDoItem"]] = relationship(back_populates="list")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="lists")


class ToDoItem(db.Model):
    __tablename__ = "items"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, unique=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    last_updated: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    list_id: Mapped[str] = mapped_column(ForeignKey("lists.id"))
    list: Mapped["ToDoList"] = relationship(back_populates="items")
    position: Mapped[int] = mapped_column(Integer, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    starred: Mapped[bool] = mapped_column(Boolean, nullable=True)
