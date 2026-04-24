from typing import TypeVar, Generic, Type
from abc import ABC, abstractmethod
from cores.asset import AssetLoader
from cores.logger import logger

T = TypeVar('T')

class Registry(ABC, Generic[T]):
    def __init__(self):
        self._data: dict[str, T] = {}
    
    def get(self, data_name: str) -> T | None:
        return self._data.get(data_name)
    
    def get_all(self) -> list[T]:
        return list(self._data.values())


class AssetRegistry(Registry[T]):
    """
    這是管理器的抽象類別
    管理器父類定義初始化時會讀取目標資料夾的 JSON 檔案，由於子類保存的資料物件不同，這裡做泛型
    """
    def __init__(self, model: Type[T], path: str):
        super().__init__()
        self._model = model
        self._path = path
        self._load()
    
    def _load(self):
        try:
            self._data: dict[str, T] = AssetLoader.load(self._path, self._model)
        except FileNotFoundError as e:
            logger.error("資料夾不存在或存在錯誤，無法讀取資料，請檢查資料夾路徑是否正確，資料字典將留空。")
            self._data = {}

class ComponentRegistry(Registry[T]):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def register(self, name: str, component: T):
        pass