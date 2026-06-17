from ..extensions import db
from .base import TimestampMixin


class SiteContent(TimestampMixin, db.Model):
    """站点文案/店铺信息：key-value，店家可后台编辑。"""
    __tablename__ = "site_contents"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {"key": self.key, "value": self.value}
