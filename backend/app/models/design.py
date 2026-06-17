from ..extensions import db
from .base import TimestampMixin


class Design(TimestampMixin, db.Model):
    """一次定制的完整参数快照（用 JSON 整合，便于扩展）。"""
    __tablename__ = "designs"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    public_token = db.Column(db.String(64), unique=True, nullable=False)
    params = db.Column(db.JSON, nullable=True)
    pattern_id = db.Column(db.Integer, db.ForeignKey("patterns.id"), nullable=True)
    upload_id = db.Column(db.Integer, db.ForeignKey("uploads.id"), nullable=True)
    thumbnail_key = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {"id": self.id, "product_id": self.product_id,
                "public_token": self.public_token, "params": self.params or {},
                "pattern_id": self.pattern_id, "upload_id": self.upload_id,
                "thumbnail_key": self.thumbnail_key}
