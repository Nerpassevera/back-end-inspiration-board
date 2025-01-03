from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card


class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    owner: Mapped[str] = mapped_column(String(25))
    cards: Mapped[list["Card"]] = relationship(
        "Card", back_populates="board", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, data):
        return Board(title=data["title"], owner=data["owner"])
