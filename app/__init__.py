import os

from flask import Flask, jsonify, send_from_directory
from sqlalchemy.exc import NoResultFound
from extensions.db import db
from flask_jwt_extended import JWTManager
from config import DevConfig, ProdConfig

# 静态前端页面放在项目根目录的 static/ 下
_STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

configs = {
    "dev": DevConfig,
    "prod": ProdConfig,
}

def create_app(profile="dev"):
    app = Flask(__name__, static_folder=_STATIC_DIR)

    app.config.from_object(configs[profile])

    if profile == "prod" and not app.config.get("JWT_SECRET_KEY"):
        raise RuntimeError("生产环境必须设置 JWT_SECRET_KEY 环境变量！")

    db.init_app(app)
    jwt = JWTManager(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"code": 4404, "msg": "接口不存在", "data": None}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"code": 4405, "msg": "请求方法不允许", "data": None}), 405

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"code": 4401, "msg": "未登录或 token 已失效", "data": None}), 401

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"code": 4500, "msg": "服务器内部错误", "data": None}), 500

    @app.get("/")
    def index():
        # 静态前端页面（原生 JS 单页，调 /api 下的 RESTful 接口）
        return send_from_directory(app.static_folder, "index.html")

    from app.routes.auth import bp_auth
    from app.routes.todo import bp_todo

    app.register_blueprint(bp_auth, url_prefix="/api/auth")
    app.register_blueprint(bp_todo, url_prefix="/api/todo")

    from app.utils.logger import setup_logger
    setup_logger(app)

    return app