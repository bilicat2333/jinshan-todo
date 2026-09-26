from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
from datetime import datetime


class Todo(db.Model):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    done: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)

    content: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), index=True)

    # Python 侧属性名为 owner（便于写 todo.owner.username），库列名仍是 user_id
    owner: Mapped["User"] = relationship(
        "User", back_populates="todos", lazy="selectin"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "done": self.done,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<Todo {self.id} {self.title}>"