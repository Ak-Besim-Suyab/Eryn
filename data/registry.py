""" 此函式庫用於定義資料註冊物件
"""
from copy import deepcopy
from lib.utils import file
from cores import logger
from data.schema import Container, Role, Item, Resource

class Storage:
    def __init__(self, path: str):
        self._path = path
        self._storage = {}

        self.load()

    def load(self):
        self._storage = file.load_dir(self._path)
        if not self._storage:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

    # 取得單筆資料
    def get(self, name: str):
        pass

    # 取得符合條件的所有資料, filters 為不定長度位置參數, 可填入多個條件, 參數名稱要對應查詢項目
    def find(self, **filters):
        pass

class ItemStorage(Storage):
    def __init__(self, path: str = "data/items"):
        super().__init__(path)

    def get(self, name: str):
        data = self._storage.get(name)
        if not data:
            return None
        
        return Item(**deepcopy(data))

    def find_flag(self, **flags):
        """返回符合所有 flags 標籤的物品
        """
        matchs = []
        for data in self._storage.values():
            item = Item(**deepcopy(data))
            if all(getattr(item.flags, key) == value for key, value in flags.items()):
                matchs.append(item)

        return matchs

class ResourceStorage(Storage):
    def __init__(self, path: str = "data/resources"):
        super().__init__(path)

    def get(self, name: str):
        data = self._storage.get(name)
        if not data:
            return None
        
        return Resource(**deepcopy(data))

class ContainerStorage(Storage):
    def __init__(self, path: str = "data/containers"):
        super().__init__(path)

    def get(self, name: str):
        data = self._storage.get(name)
        if not data:
            return None
        
        return Container(**deepcopy(data))

class RoleStorage(Storage):
    def __init__(self, path: str = "data/roles"):
        super().__init__(path)

    def get(self, name: str):
        data = self._storage.get(name)
        if not data:
            return None
        
        return Role(**deepcopy(data))
    
    def get_all(self):
        return [Role(**deepcopy(data)) for data in self._storage.values()]
    
    # 例如: 找查特定分類時, 填入 (category = "specific_category"), 找查特定標籤時, 填入 (tag = "specific_tag")
    def find(self, **filters) -> list[Role]:
        return [Role(**deepcopy(data)) for data in self._storage.values() if all(data.get(key) == value for key, value in filters.items())]

item = ItemStorage()
resource = ResourceStorage()
container = ContainerStorage()
role = RoleStorage()