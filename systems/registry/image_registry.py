"""
該類別的單例宣告於 registries/__init__.py 中, 以避免循環引用問題
"""
from cores import AssetRegistry

from models import Image

class ImageRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(path = "assets/images")

    def get(self, image_id: str):
        data = self._data.get(image_id)
        if not data:
            return None

        return Image(**data)