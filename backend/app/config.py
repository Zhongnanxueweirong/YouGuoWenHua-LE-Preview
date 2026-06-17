"""配置类：按环境区分。所有可变项走环境变量(12-factor)。"""
import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    # 默认 sqlite 便于本地裸跑；docker-compose 内通过环境变量指向 MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(os.getcwd(), "data", "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # 存储
    STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local")  # local | s3
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(os.getcwd(), "data", "uploads"))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_MB", "8")) * 1024 * 1024

    # 站点 / 后台
    PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "http://localhost")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin888")

    # session cookie
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # 生产走 HTTPS


def get_config():
    env = os.environ.get("FLASK_ENV", "production").lower()
    return DevConfig if env in ("development", "dev") else ProdConfig
