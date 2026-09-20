from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db


class Todo(db.Model):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    done: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)

    # 库里真实列名就是 user_id，别再写成 owner_id
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), index=True)

    # Python 侧叫 owner 方便取 todo.owner.username，库列还是 user_id
    owner: Mapped["User"] = relationship(
        "User", back_populates="todos", lazy="selectin"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "owner_id": self.user_id,
            "owner": self.owner.username if self.owner else None,
        }

    def __repr__(self) -> str:
        return f"<Todo {self.id} {self.title}>"