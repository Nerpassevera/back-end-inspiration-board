from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board
class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(255))
    likes_count: Mapped[int] # dont forget to set defalt to 0
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="cards")


    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
    }

    @classmethod
    def from_dict(cls, data):
        return Card(message=data["message"], likes_count=0, board_id=1)