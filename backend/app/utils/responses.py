"""统一响应结构：{ code, message, data }。code=0 表示成功。"""
from flask import jsonify


def ok(data=None, message="ok"):
    return jsonify({"code": 0, "message": message, "data": data})


def fail(message, code=40000, http_status=400, data=None):
    resp = jsonify({"code": code, "message": message, "data": data})
    resp.status_code = http_status
    return resp


def paginate(query, page, page_size):
    page = max(1, int(page or 1))
    page_size = min(100, max(1, int(page_size or 20)))
    total = query.count()
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    return items, total, page, page_size
