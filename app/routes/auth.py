import re

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from extensions.db import db
from app.models import User
from app.utils.response import fail, ok

# 蓝图在路由模块内创建，不反向导入 app，避免循环导入
bp_auth = Blueprint("auth", __name__)


@bp_auth.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return fail("账号密码不能空", 4001, 400)

    user = db.session.scalars(select(User).where(User.username == username)).first()
    if not user or not user.check_password(password):
        return fail("账号或密码错", 4002, 401)

    # identity 必须是字符串，读出来时再还原成 int
    token = create_access_token(identity=str(user.id))

    return ok({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
        },
    }, "登录成功")


@bp_auth.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    nickname = (data.get("nickname") or "").strip()
    password = data.get("password") or ""

    # 参数校验：用户名规则 + 密码长度（哈希由 User.password setter 统一处理）
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username):
        return fail("用户名需为 3-20 位字母/数字/下划线", 4201, 400)
    if len(password) < 6:
        return fail("密码至少 6 位", 4201, 400)

    # 先查后插只用于给出友好提示；并发下的唯一性由 username 上的唯一索引兜底
    exists = db.session.scalars(
        select(User).where(User.username == username)
    ).first()
    if exists:
        return fail("用户名已被占用", 4005, 409)

    user = User(username=username, nickname=nickname or username)
    user.password = password  # setter 内自动哈希，库里只存密文
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail("用户名已被占用", 4005, 409)

    # 注册成功直接发 token，省一次登录
    token = create_access_token(identity=str(user.id))
    return ok({
        "token": token,
        "user": {"id": user.id, "username": user.username, "nickname": user.nickname},
    }, "注册成功"), 201


@bp_auth.get("/me")
@jwt_required()
def me():
    uid = int(get_jwt_identity())
    user = db.session.scalars(
        select(User).where(User.id == uid).options(
            joinedload(User.department),
            joinedload(User.extension),
        )
    ).unique().one_or_none()

    if not user:
        return fail("用户不在了", 4004, 404)

    return ok({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "department": user.department.name if user.department else None,
        "student_no": user.extension.student_no if user.extension else None,
    })
