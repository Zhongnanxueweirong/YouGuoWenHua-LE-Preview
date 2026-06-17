from ..extensions import db
from .base import TimestampMixin

# 状态常量（用字符串而非 DB 枚举，便于将来扩展且跨库可移植）
ORDER_STATUSES = ["new", "contacted", "confirmed", "producing", "completed", "cancelled"]
PAYMENT_STATUSES = ["unpaid", "paid_offline", "paid_online"]


class Order(TimestampMixin, db.Model):
    """订单 / 定制意向：统一承载留资咨询与下单意向。"""
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(32), unique=True, nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    wechat = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    design_id = db.Column(db.Integer, db.ForeignKey("designs.id"), nullable=True)
    status = db.Column(db.String(20), default="new", nullable=False)
    source = db.Column(db.String(30), default="web", nullable=False)
    payment_status = db.Column(db.String(20), default="unpaid", nullable=False)  # 预留
    operator_note = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {"id": self.id, "order_no": self.order_no,
                "contact_name": self.contact_name, "phone": self.phone,
                "wechat": self.wechat, "message": self.message,
                "quantity": self.quantity, "product_id": self.product_id,
                "design_id": self.design_id, "status": self.status,
                "source": self.source, "payment_status": self.payment_status,
                "operator_note": self.operator_note,
                "created_at": self.created_at.isoformat() if self.created_at else None}
