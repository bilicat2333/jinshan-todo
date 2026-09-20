from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# ✅ 蓝图就在这创建，不从 app 里 import（之前那行就是死循环式报错）
bp_auth = Blueprint("auth", __name__)

from extensions.db import db          # 放下面导入避免循环（惯例这么写没事）
from app.models import User


@bp_auth.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify(code=4001, msg="账号密码不能空"), 400

    user = db.session.scalars(select(User).where(User.username == username)).first()
    if not user or not user.check_password(password):
        return jsonify(code=4002, msg="账号或密码错"), 401

    # ✅ 铁律：identity 只给 str(id)
    token = create_access_token(identity=str(user.id))

    return jsonify(code=0, msg="登录成功", data={
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
        },
    })


@bp_auth.get("/me")
@jwt_required()
def me():
    uid = int(get_jwt_identity())     # "1" → 1
    user = db.session.scalars(
        select(User).where(User.id == uid).options(
            joinedload(User.department),
            joinedload(User.extension),
        )
    ).unique().one_or_none()

    if not user:
        return jsonify(code=4004, msg="用户不在了"), 404

    return jsonify(code=0, msg="ok", data={
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "department": user.department.name if user.department else None,
        "student_no": user.extension.student_no if user.extension else None,
    })