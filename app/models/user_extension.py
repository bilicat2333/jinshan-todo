from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
# ❌ 删掉：from app.models.user import User
# 改成：User 用字符串 "User"，运行时才解析，不参与导入环


class UserExtension(db.Model):
    __tablename__ = "user_extension"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    # unique=True 是一对一的命门，少了就退化成一堆多
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    student_no: Mapped[str | None] = mapped_column(db.String(30))
    phone: Mapped[str | None] = mapped_column(db.String(20))

    # ✅ 字符串 "User" → 不触发导入 → 循环直接断
    user: Mapped["User"] = relationship("User", back_populates="extension")

    def __repr__(self) -> str:
        return f"<UserExtension uid={self.user_id}>"