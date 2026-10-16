from lib import file
from cores.logger import logger

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
        return self._data.get(name)

class ContainerData(Data):
    def __init__(self, path: str = "data/containers"):
        super().__init__(path)