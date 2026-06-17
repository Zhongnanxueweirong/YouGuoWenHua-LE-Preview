from flask import Blueprint, request
from ..models import Pattern
from ..utils.responses import ok

bp = Blueprint("patterns", __name__, url_prefix="/patterns")


@bp.get("")
def list_patterns():
    q = Pattern.query.filter_by(is_active=True)
    pid = request.args.get("product_id", type=int)
    if pid:
        q = q.filter_by(product_id=pid)
    rows = q.order_by(Pattern.sort_order).all()
    return ok([p.to_dict() for p in rows])
