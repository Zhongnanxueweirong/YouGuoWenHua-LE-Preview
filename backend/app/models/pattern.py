from ..extensions import db
from .base import TimestampMixin


class Pattern(TimestampMixin, db.Model):
    """祈福图样素材库（定制器用）。"""
    __tablename__ = "patterns"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    image_key = db.Column(db.String(500), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "key": self.key, "name": self.name,
                "description": self.description, "image_key": self.image_key,
                "product_id": self.product_id, "sort_order": self.sort_order,
                "is_active": self.is_active}
