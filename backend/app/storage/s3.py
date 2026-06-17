"""S3 兼容存储（MinIO/OBS/OSS/COS/R2）——第1期实现。
占位：届时用 boto3，凭 .env 的 S3_ENDPOINT/S3_BUCKET/S3_ACCESS_KEY/S3_SECRET_KEY 接入。
"""
from .base import Storage


class S3Storage(Storage):  # pragma: no cover
    def __init__(self):
        raise NotImplementedError("S3 存储为第1期功能，尚未实现")

    def save(self, file_obj, key): ...
    def url(self, key): ...
    def delete(self, key): ...
