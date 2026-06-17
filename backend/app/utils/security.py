"""鉴权工具：极简单密码 + session。"""
from functools import wraps
from flask import session
from .responses import fail


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return fail("未登录或登录已过期", code=40100, http_status=401)
        return view(*args, **kwargs)
    return wrapper
