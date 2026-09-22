from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db


class UserExtension(db.Model):
    __tablename__ = "user_extension"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    # unique=True 保证这里是一对一，缺少就会退化成一堆多
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    student_no: Mapped[str | None] = mapped_column(db.String(30))
    phone: Mapped[str | None] = mapped_column(db.String(20))

    # 用字符串引用 User，运行时才解析，不参与导入环
    user: Mapped["User"] = relationship("User", back_populates="extension")

    def __repr__(self) -> str:
        return f"<UserExtension uid={self.user_id}>"