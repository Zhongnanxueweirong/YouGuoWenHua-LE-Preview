from flask import Blueprint
from ..models import SiteContent
from ..utils.responses import ok, fail

bp = Blueprint("content", __name__, url_prefix="/content")


@bp.get("/<key>")
def get_content(key):
    row = SiteContent.query.filter_by(key=key).first()
    if not row:
        return fail("内容不存在", code=40400, http_status=404)
    return ok(row.to_dict())
