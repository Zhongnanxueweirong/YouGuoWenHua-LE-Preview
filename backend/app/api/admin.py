"""后台接口：极简单密码 + session。面向年长操作者，前端做大字大按钮。"""
from flask import Blueprint, request, session, current_app
from ..schemas.order import OrderStatusUpdate
from ..services import order_service, stats_service
from ..utils.responses import ok, fail
from ..utils.security import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if data.get("password") == current_app.config["ADMIN_PASSWORD"]:
        session["is_admin"] = True
        return ok({"login": True})
    return fail("密码不正确", code=40100, http_status=401)


@bp.post("/logout")
def logout():
    session.clear()
    return ok({"logout": True})


@bp.get("/orders")
@login_required
def list_orders():
    status = request.args.get("status")
    rows = order_service.list_orders(status=status).all()
    return ok([o.to_dict() for o in rows])


@bp.patch("/orders/<int:oid>")
@login_required
def update_order(oid):
    payload = OrderStatusUpdate(**(request.get_json(silent=True) or {}))
    order = order_service.update_order(
        oid, status=payload.status, operator_note=payload.operator_note)
    return ok(order.to_dict())


@bp.get("/stats")
@login_required
def stats():
    return ok(stats_service.summary())
