""" 此函示庫用於定義資料結構
"""
from copy import deepcopy

from lib import file

from cores.logger import logger

from data.schema import Container, Role

class Data:
    def __init__(self, path: str):
        self._path = path
        self._data = {}

        self.load()

    def load(self):
        self._data = file.load_dir(self._path)
        if not self._data:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

    # 取得單筆資料
    def get(self, name: str):
        pass

    # 取得符合條件的所有資料, filters 為不定長度位置參數, 可填入多個條件, 參數名稱要對應查詢項目
    def find(self, **filters):
        pass

class ContainerData(Data):
    def __init__(self, path: str = "data/res/containers"):
        super().__init__(path)

    def get(self, name: str):
        data = self._data.get(name)
        if not data:
            return None
        
        return Container(**deepcopy(data))

class RoleData(Data):
    def __init__(self, path: str = "data/res/roles"):
        super().__init__(path)

    def get(self, name: str):
        data = self._data.get(name)
        if not data:
            return None
        
        return Role(**deepcopy(data))
    
    def get_all(self):
        return [Role(**deepcopy(data)) for data in self._data.values()]
    
    # 例如: 找查特定分類時, 填入 (category = "specific_category"), 找查特定標籤時, 填入 (tag = "specific_tag")
    def find(self, **filters) -> list[Role]:
        return [Role(**deepcopy(data)) for data in self._data.values() if all(data.get(key) == value for key, value in filters.items())]
