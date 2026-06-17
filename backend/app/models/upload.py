from ..extensions import db
from .base import TimestampMixin


class Upload(TimestampMixin, db.Model):
    __tablename__ = "uploads"
    id = db.Column(db.Integer, primary_key=True)
    storage_key = db.Column(db.String(500), nullable=False)
    mime = db.Column(db.String(100), nullable=True)
    size = db.Column(db.Integer, nullable=True)
    ip_hash = db.Column(db.String(64), nullable=True)

    def to_dict(self):
        return {"id": self.id, "storage_key": self.storage_key,
                "mime": self.mime, "size": self.size}
