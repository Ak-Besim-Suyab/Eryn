from typing import TypeVar, Generic, Type
from cores.loader import AssetLoader
from cores.logger import logger

T = TypeVar('T')

class Registry(Generic[T]):
    """
    這是管理器的抽象類別
    管理器父類定義初始化時會讀取目標資料夾的 JSON 檔案，由於子類保存的資料物件不同，這裡做泛型
    """
    def __init__(self, model: Type[T], path: str):
        self._data: dict[str, T] = {}
        self._model = model
        self._path = path
        self._load()
    
    def _load(self):
        try:
            self._data: dict[str, T] = AssetLoader.load(self._path, self._model)
        except FileNotFoundError as e:
            logger.error("資料夾不存在或存在錯誤，無法讀取資料，請檢查資料夾路徑是否正確，資料字典將留空。")
            self._data = {}

    def get(self, object_id: str) -> T | None:
        return self._data.get(object_id)

    def get_all(self) -> list[T]:
        return list(self._data.values())