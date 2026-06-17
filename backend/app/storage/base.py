"""存储接口：所有后端实现一致，业务层只依赖此接口。"""
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, file_obj, key: str) -> str:
        """保存文件，返回可对外访问的 url。"""

    @abstractmethod
    def url(self, key: str) -> str:
        """由 key 得到访问 url。"""

    @abstractmethod
    def delete(self, key: str) -> None:
        ...
