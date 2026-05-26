"""
該類別的單例宣告於 registries/__init__.py 中, 以避免循環引用問題
"""
from cores import AssetRegistry
import models

class RoleRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(path = "assets/roles")

    def get(self, role_id: str):
        data = self._data.get(role_id)
        if not data:
            return None
        
        return models.Role(**data)
    
    def get_all(self):
        return [models.Role(**data) for data in self._data.values()]