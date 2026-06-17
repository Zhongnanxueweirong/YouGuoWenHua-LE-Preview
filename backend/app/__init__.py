"""应用工厂。所有初始化集中于此，便于测试与扩展。"""
import os
from flask import Flask
from .config import get_config
from .extensions import db, migrate, cors
from .errors import register_error_handlers


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())

    # 确保本地存储与 sqlite 目录存在
    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    # 导入模型(供 Alembic 发现) + 注册蓝图
    from . import models  # noqa: F401
    from .api import register_blueprints
    register_blueprints(app)
    register_error_handlers(app)

    register_cli(app)
    return app


def register_cli(app):
    @app.cli.command("seed")
    def seed():
        """灌入初始数据(分类/示例商品/素材/店铺文案)。"""
        from scripts.seed import run_seed
        run_seed()
        print("seed done.")
