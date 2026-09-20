# app/models/permission.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
from app.models.department_permission import department_permission as _m2m   # ✅ 同一个 Table


class Permission(db.Model):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    code: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(db.String(50), nullable=False)

    # ✅ 反向属性就叫 departments，和上面 back_populates="departments" 严丝合缝
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary=_m2m,
        back_populates="permissions",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Permission {self.code}>"