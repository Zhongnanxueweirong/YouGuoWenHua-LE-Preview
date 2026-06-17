"""订单/留资业务逻辑。路由只调用这里，不直接操作模型。"""
from datetime import datetime
from ..extensions import db
from ..models import Order
from ..models.order import ORDER_STATUSES
from ..errors import ApiError


def _gen_order_no():
    today = datetime.utcnow().strftime("%Y%m%d")
    start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    count_today = Order.query.filter(Order.created_at >= start).count()
    return f"YG{today}-{count_today + 1:04d}"


def create_order(data: dict) -> Order:
    order = Order(
        order_no=_gen_order_no(),
        contact_name=data["contact_name"],
        phone=data["phone"],
        wechat=data.get("wechat"),
        message=data.get("message"),
        quantity=data.get("quantity"),
        product_id=data.get("product_id"),
        design_id=data.get("design_id"),
        source=data.get("source") or "web",
        status="new",
    )
    db.session.add(order)
    db.session.commit()
    return order


def list_orders(status=None):
    q = Order.query
    if status:
        q = q.filter(Order.status == status)
    return q.order_by(Order.created_at.desc())


def update_order(order_id: int, status=None, operator_note=None) -> Order:
    order = Order.query.get(order_id)
    if not order:
        raise ApiError("订单不存在", code=40400, http_status=404)
    if status is not None:
        if status not in ORDER_STATUSES:
            raise ApiError("非法的订单状态", code=42200, http_status=422)
        order.status = status
    if operator_note is not None:
        order.operator_note = operator_note
    db.session.commit()
    return order
