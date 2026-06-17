"""存储抽象工厂：按 STORAGE_BACKEND 返回实现。"""
from flask import current_app
from .local import LocalStorage

_instance = None


def get_storage():
    global _instance
    if _instance is None:
        backend = current_app.config.get("STORAGE_BACKEND", "local")
        if backend == "s3":
            from .s3 import S3Storage  # 第1期再实现，按需导入
            _instance = S3Storage()
        else:
            _instance = LocalStorage()
    return _instance
