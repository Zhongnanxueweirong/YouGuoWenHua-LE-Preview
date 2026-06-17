from ..extensions import db
from .base import TimestampMixin


class Product(TimestampMixin, db.Model):
    """平台中心实体。type 决定用哪个前端模块展示；config 存类型专属配置。"""
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    type = db.Column(db.String(50), nullable=False, default="laser_customizer")
    name = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300), nullable=True)
    cover_key = db.Column(db.String(500), nullable=True)
    config = db.Column(db.JSON, nullable=True)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self, full=False):
        d = {"id": self.id, "category_id": self.category_id, "type": self.type,
             "name": self.name, "subtitle": self.subtitle, "cover_key": self.cover_key,
             "sort_order": self.sort_order, "is_active": self.is_active}
        if full:
            d["config"] = self.config or {}
        return d
