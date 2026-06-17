"""全局错误处理：统一错误结构，避免泄漏堆栈。"""
from pydantic import ValidationError
from .utils.responses import fail


class ApiError(Exception):
    def __init__(self, message, code=40000, http_status=400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def _api_error(e):
        return fail(e.message, code=e.code, http_status=e.http_status)

    @app.errorhandler(ValidationError)
    def _validation(e):
        first = e.errors()[0] if e.errors() else {}
        loc = ".".join(str(x) for x in first.get("loc", []))
        msg = first.get("msg", "参数校验失败")
        return fail(f"{loc}: {msg}".strip(": "), code=42200, http_status=422)

    @app.errorhandler(404)
    def _404(e):
        return fail("资源不存在", code=40400, http_status=404)

    @app.errorhandler(405)
    def _405(e):
        return fail("请求方法不被允许", code=40500, http_status=405)

    @app.errorhandler(500)
    def _500(e):
        return fail("服务器内部错误", code=50000, http_status=500)
