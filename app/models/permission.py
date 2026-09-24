# app/models/permission.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
from app.models.department_permission import department_permission as _m2m   # 与 Department 复用同一张关联表


class Permission(db.Model):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    code: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    label: Mapped[str] = mapped_column(db.String(50), nullable=False)

    # 反向属性，与 Department.permissions 的 back_populates 对应
    departments: Mapped[list["Department"]] = relationship(
        "Department",
        secondary=_m2m,
        back_populates="permissions",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Permission {self.code}>"