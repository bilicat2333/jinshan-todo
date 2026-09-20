from flask import Flask
from extensions.db import db
from config import DevConfig, ProdConfig

configs = {
    "dev": DevConfig,
    "prod": ProdConfig,
}

def create_app(profile="dev"):
    app = Flask(__name__)

    app.config.from_object(configs[profile])

    # 生产环境强制要求 JWT 密钥
    if profile == "prod" and not app.config.get("JWT_SECRET_KEY"):
        raise RuntimeError("生产环境必须设置 JWT_SECRET_KEY 环境变量！")

    db.init_app(app)

    from app.routes.auth import bp_auth
    from app.routes.todo import bp_todo

    app.register_blueprint(bp_auth, url_prefix="/api/auth")
    app.register_blueprint(bp_todo, url_prefix="/api/todo")

    return app