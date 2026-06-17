from flask import Blueprint
from ..models import Category
from ..utils.responses import ok

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.get("")
def list_categories():
    rows = (Category.query.filter_by(is_active=True)
            .order_by(Category.sort_order).all())
    return ok([c.to_dict() for c in rows])
