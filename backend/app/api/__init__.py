"""把所有蓝图注册到 /api/v1。新增资源=新增一个蓝图文件并在此登记。"""
from flask import Blueprint

from .categories import bp as categories_bp
from .products import bp as products_bp
from .patterns import bp as patterns_bp
from .designs import bp as designs_bp
from .uploads import bp as uploads_bp
from .orders import bp as orders_bp
from .content import bp as content_bp
from .share import bp as share_bp
from .admin import bp as admin_bp


def register_blueprints(app):
    api = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    for bp in (categories_bp, products_bp, patterns_bp, designs_bp,
               uploads_bp, orders_bp, content_bp, share_bp, admin_bp):
        api.register_blueprint(bp)
    app.register_blueprint(api)

    @app.get("/api/health")
    def health():
        return {"code": 0, "message": "ok", "data": {"status": "healthy"}}
