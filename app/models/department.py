# app/models/department.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions.db import db
from app.models.department_permission import department_permission as _m2m   # 多对多关联表


class Department(db.Model):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    remark: Mapped[str | None] = mapped_column(db.String(200))

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="department", lazy="select"
    )

    # 多对多：secondary 指向关联表，反向属性由 Permission.departments 承接
    # 权限是预留功能，暂无接口使用，保持默认懒加载避免每次加载部门都连带查权限
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=_m2m,
        back_populates="departments",
    )

    def __repr__(self) -> str:
        return f"<Department {self.name}>"