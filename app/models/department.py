# app/models/department.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
from app.models.department_permission import department_permission as _m2m   # ✅ 拿 Table


class Department(db.Model):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    remark: Mapped[str | None] = mapped_column(db.String(200))

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="department", lazy="selectin"
    )

    # ✅ 正向就写在这里，secondary 是 Table，back_populates 叫 "departments"
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=_m2m,
        back_populates="departments",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Department {self.name}>"