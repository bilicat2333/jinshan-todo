# app/models/user.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.db import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False, index=True)
    nickname: Mapped[str | None] = mapped_column(db.String(50), default="新同学")

    # Python 属性名与库列名刻意分离：库里存哈希，外部拿不到明文
    _password_hash: Mapped[str] = mapped_column("password", db.String(255), nullable=False)

    department_id: Mapped[int | None] = mapped_column(db.ForeignKey("department.id"))
    department: Mapped["Department"] = relationship(
        "Department", back_populates="users", lazy="selectin"
    )

    extension: Mapped["UserExtension"] = relationship(
        "UserExtension", back_populates="user", cascade="all, delete-orphan", lazy="selectin", uselist=False
    )
    # 集合关系不用 selectin：待办可能很多，且多数接口用不到，按需加载即可
    todos: Mapped[List["Todo"]] = relationship(
        "Todo", back_populates="owner", cascade="all, delete-orphan"
    )

    # ─── 保险箱：只能写、不能读 ───
    @property
    def password(self) -> str:
        raise AttributeError("密码不能明文读！校验请用 check_password()")

    @password.setter
    def password(self, raw: str) -> None:
        if not raw or len(raw) < 6:
            raise ValueError("密码至少 6 位～")
        self._password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        if not raw or not self._password_hash:
            return False
        return check_password_hash(self._password_hash, raw)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "department": self.department.name if self.department else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"