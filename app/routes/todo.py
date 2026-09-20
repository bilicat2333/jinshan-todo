from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.orm import joinedload

bp_todo = Blueprint("todo", __name__)

from extensions.db import db
from app.models import Todo, User
from app.utils.response import ok, fail


@bp_todo.post("")
@bp_todo.post("/")
@jwt_required()
def create_todo():
    uid = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return fail("待办标题不能空", 4201, 400)

    todo = Todo(title=title, user_id=uid)
    db.session.add(todo)
    db.session.commit()
    return ok({"id": todo.id, "title": todo.title}, "建好了", 0), 201


@bp_todo.get("")
@bp_todo.get("/")
@jwt_required()
def list_todo():
    uid = int(get_jwt_identity())
    rows = db.session.scalars(
        select(Todo).where(Todo.user_id == uid).order_by(Todo.id.desc())
    ).unique().all()

    return ok({
        "total": len(rows),
        "items": [
            {"id": t.id, "title": t.title, "done": t.done, "owner": t.owner.username}
            for t in rows
        ],
    })


@bp_todo.get("/<int:todo_id>")
@jwt_required()
def one_todo(todo_id: int):
    uid = int(get_jwt_identity())
    todo = db.session.scalars(
        select(Todo)
        .where(Todo.id == todo_id, Todo.user_id == uid)
        .options(joinedload(Todo.owner))
    ).unique().one_or_none()

    if not todo:
        return fail("这条不是你的，或压根不存在", 4104, 403)

    return ok({
        "id": todo.id,
        "title": todo.title,
        "done": todo.done,
        "owner": todo.owner.username,
        "dept": todo.owner.department.name if todo.owner.department else None,
    })


@bp_todo.patch("/<int:todo_id>")
@jwt_required()
def update_todo(todo_id: int):
    uid = int(get_jwt_identity())

    todo = db.session.get(Todo, todo_id)
    if not todo:
        return fail("待办不存在", 4404, 404)

    if todo.user_id != uid:
        return fail("无权操作别人的待办", 4104, 403)

    data = request.get_json(silent=True) or {}
    if "done" in data:
        todo.done = bool(data["done"])
    if "title" in data and str(data["title"]).strip():
        todo.title = str(data["title"]).strip()

    db.session.commit()
    return ok({"id": todo.id, "title": todo.title, "done": todo.done}, "改好了")


@bp_todo.delete("/<int:todo_id>")
@jwt_required()
def delete_todo(todo_id: int):
    uid = int(get_jwt_identity())

    todo = db.session.get(Todo, todo_id)
    if not todo:
        return fail("待办不存在", 4404, 404)

    if todo.user_id != uid:
        return fail("无权删除别人的待办", 4104, 403)

    db.session.delete(todo)
    db.session.commit()
    return ok(None, "删掉了")