"""本地卷存储：最省、可移植(搬服务器=拷文件夹)。Caddy 负责对外暴露 /uploads。"""
import os
from flask import current_app
from .base import Storage


class LocalStorage(Storage):
    def _root(self):
        return current_app.config["UPLOAD_DIR"]

    def save(self, file_obj, key: str) -> str:
        path = os.path.join(self._root(), key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_obj.save(path)
        return self.url(key)

    def save_bytes(self, data: bytes, key: str) -> str:
        path = os.path.join(self._root(), key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return self.url(key)

    def url(self, key: str) -> str:
        base = current_app.config.get("PUBLIC_BASE_URL", "").rstrip("/")
        return f"{base}/uploads/{key}"

    def delete(self, key: str) -> None:
        path = os.path.join(self._root(), key)
        if os.path.exists(path):
            os.remove(path)
