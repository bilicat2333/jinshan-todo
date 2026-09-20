from extensions.db import db

department_permission = db.Table(
    "department_permission",
    db.Column("department_id", db.Integer, db.ForeignKey("department.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True),
)