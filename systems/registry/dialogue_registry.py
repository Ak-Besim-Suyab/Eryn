"""
該類別的單例宣告於 registries/__init__.py 中, 以避免循環引用問題
"""
from cores import AssetRegistry

from models import Dialogue

class DialogueRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(path = "assets/dialogues")

    def get(self, dialogue_id: str):
        data = self._data.get(dialogue_id)
        if not data:
            return None

        return Dialogue(**data)