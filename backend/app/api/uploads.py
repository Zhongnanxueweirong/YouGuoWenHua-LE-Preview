import hashlib
import secrets
import os
from flask import Blueprint, request
from ..extensions import db
from ..models import Upload
from ..storage import get_storage
from ..utils.responses import ok, fail

bp = Blueprint("uploads", __name__, url_prefix="/uploads")

ALLOWED = {"image/png", "image/jpeg", "image/webp", "image/gif"}


@bp.post("")
def upload():
    f = request.files.get("file")
    if not f:
        return fail("未收到文件", code=40000, http_status=400)
    if f.mimetype not in ALLOWED:
        return fail("仅支持图片(png/jpg/webp/gif)", code=40000, http_status=400)
    ext = os.path.splitext(f.filename or "")[1].lower() or ".png"
    key = f"img/{secrets.token_hex(8)}{ext}"
    url = get_storage().save(f, key)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "")
    rec = Upload(storage_key=key, mime=f.mimetype, size=None,
                 ip_hash=hashlib.sha256(ip.encode()).hexdigest()[:64])
    db.session.add(rec)
    db.session.commit()
    return ok({"id": rec.id, "url": url, "storage_key": key})
