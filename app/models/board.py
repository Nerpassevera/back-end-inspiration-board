from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db import db

class Board(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String(50))
    owner:Mapped[str] = mapped_column(String(25))
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, data):
        return Board(title=data["title"], owner=data["owner"])
