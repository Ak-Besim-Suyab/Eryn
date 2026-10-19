from copy import deepcopy

from lib import file

from cores.logger import logger

from schema.container import Container
from schema.role import Role

class Data:
    def __init__(self, path: str):
        self._path = path
        self._data = {}

        self.load()

    def load(self):
        self._data = file.load_dir(self._path)
        if not self._data:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

    def get(self, name: str):
        pass

class ContainerData(Data):
    def __init__(self, path: str = "data/containers"):
        super().__init__(path)

    def get(self, name: str):
        data = self._data.get(name)
        if not data:
            return None
        
        return Container(**deepcopy(data))

class RoleData(Data):
    def __init__(self, path: str = "data/roles"):
        super().__init__(path)

    def get(self, name: str):
        data = self._data.get(name)
        if not data:
            return None
        
        return Role(**deepcopy(data))

    def get_all(self):
        return [Role(**deepcopy(data)) for data in self._data.values()]