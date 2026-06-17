import secrets
from ..extensions import db
from ..models import Design
from ..errors import ApiError


def create_design(data: dict) -> Design:
    design = Design(
        product_id=data.get("product_id"),
        public_token=secrets.token_urlsafe(12),
        params=data.get("params") or {},
        pattern_id=data.get("pattern_id"),
        upload_id=data.get("upload_id"),
    )
    db.session.add(design)
    db.session.commit()
    return design


def get_by_token(token: str) -> Design:
    design = Design.query.filter_by(public_token=token).first()
    if not design:
        raise ApiError("设计不存在或已失效", code=40400, http_status=404)
    return design
