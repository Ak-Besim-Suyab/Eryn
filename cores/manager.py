from typing import TypeVar, Generic, Type
from cores.loader import JsonLoader
from cores.logger import logger

T = TypeVar('T')

class Manager(Generic[T]):
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
        raw_data = JsonLoader.load(self._path)
        if not raw_data:
            logger.error(f"找不到資料夾: {self._path}")
            return

        total_files = 0
        for filename, data in raw_data.items():
            if not isinstance(data, dict):
                logger.error(f"JSON 檔案格式出現錯誤: {filename}")
                continue

            try:
                obj = self._model(**data)
                self._data[obj.id] = obj
                total_files += 1
                logger.info(f"載入檔案成功: {filename}.json")

            except TypeError as e:
                logger.error(f"{filename} 的 JSON 格式與 {self._model.__name__} 類別不相容: {e}")
                continue
        
        logger.info(f"資料載入完畢，總共載入 {total_files} 個檔案")

    def get(self, object_id: str) -> T | None:
        return self._data.get(object_id)

    def get_all(self) -> list[T]:
        return list(self._data.values())