"""
該模組定義註冊器類別, 註冊器用於

.. note::
    目前將讀取檔案的錯誤拋出都移至 asset 模組, 註冊器則專注於處理資料結構的錯誤
"""
from typing import TypeVar
from abc import ABC
from cores import asset
from cores.logger import logger

T = TypeVar("T")

class Registry(ABC):
    def __init__(self):
        self._data = {}

    def get(self, name: str):
        return self._data.get(name)

    def get_all(self):
        pass

class AssetRegistry(Registry):
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._load()
    
    def _load(self):
        self._data = asset.load(self._path)
        if not self._data:
            logger.warning(f"路徑所取得的資料為空: {self._path}")