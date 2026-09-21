from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import re

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


@bp_auth.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    nickname = (data.get("nickname") or "").strip()
    password = data.get("password") or ""

    # 参数校验：用户名规则 + 密码长度（哈希由 User.password setter 统一处理）
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        return jsonify(code=4201, msg="用户名需为 3-20 位字母/数字/下划线"), 400
    if len(password) < 6:
        return jsonify(code=4201, msg="密码至少 6 位"), 400

    exists = db.session.scalars(
        select(User).where(User.username == username)
    ).first()
    if exists:
        return jsonify(code=4005, msg="用户名已被占用"), 409

    user = User(username=username, nickname=nickname or username)
    user.password = password  # setter 内自动哈希，库里永远是密文
    db.session.add(user)
    db.session.commit()

    # 注册成功直接发 token，省一次登录
    token = create_access_token(identity=str(user.id))
    return jsonify(code=0, msg="注册成功", data={
        "token": token,
        "user": {"id": user.id, "username": user.username, "nickname": user.nickname},
    }), 201


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