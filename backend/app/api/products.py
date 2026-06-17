from flask import Blueprint, request
from ..models import Product
from ..utils.responses import ok, fail

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.get("")
def list_products():
    q = Product.query.filter_by(is_active=True)
    cat = request.args.get("category_id", type=int)
    if cat:
        q = q.filter_by(category_id=cat)
    rows = q.order_by(Product.sort_order).all()
    return ok([p.to_dict() for p in rows])


@bp.get("/<int:pid>")
def get_product(pid):
    p = Product.query.get(pid)
    if not p or not p.is_active:
        return fail("商品不存在", code=40400, http_status=404)
    return ok(p.to_dict(full=True))
