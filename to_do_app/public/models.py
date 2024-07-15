import datetime as dt
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String

from to_do_app.database import db


class ToDoList(db.Model):
    __tablename__ = "lists"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    items: Mapped[List["ToDoItem"]] = relationship(back_populates="list")
    # to add in: user


class ToDoItem(db.Model):
    __tablename__ = "items"
    id: Mapped[str] = mapped_column(
        String, primary_key=True, nullable=False, unique=True
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    list_id: Mapped[str] = mapped_column(ForeignKey("lists.id"))
    list: Mapped["ToDoList"] = relationship(back_populates="items")
    list_order: Mapped[int] = mapped_column(Integer, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=True)
    starred: Mapped[bool] = mapped_column(Boolean, nullable=True)
    tagged_color: Mapped[str] = mapped_column(String, nullable=True)
    due_date: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
