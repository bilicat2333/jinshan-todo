import os
from dotenv import load_dotenv

load_dotenv()


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_env('DB_USER', 'root')}:"
        f"{_env('DB_PASSWORD', '')}@"
        f"{_env('DB_HOST', '127.0.0.1')}:"
        f"{_env('DB_PORT', '3306')}/"
        f"{_env('DB_NAME', 'jinshan')}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = _env("JWT_SECRET_KEY", "dev-only-fallback-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(_env("JWT_ACCESS_TOKEN_EXPIRES", "43200"))


class ProdConfig(DevConfig):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = _env("JWT_SECRET_KEY", "")