from flask import Blueprint, request
from ..schemas.order import OrderCreate
from ..services import order_service
from ..utils.responses import ok

bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.post("")
def create_order():
    payload = OrderCreate(**(request.get_json(silent=True) or {}))
    # 蜜罐：机器人填了 hp 字段，假装成功但不入库
    if payload.hp:
        return ok({"order_no": "YG-IGNORED"})
    data = payload.model_dump(exclude={"hp"})
    order = order_service.create_order(data)
    return ok({"id": order.id, "order_no": order.order_no})
