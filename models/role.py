from dataclasses import dataclass
from cores.registry import AssetRegistry

@dataclass
class Role:
    id: str
    name: str
    icon: str
    category: str
    tag: str

class RoleManager(AssetRegistry[Role]):
    def __init__(self):
        super().__init__(
            model = Role, 
            path = "assets/roles"
        )

    def get_role_by_category(self, category: str) -> list[Role]:
        record = []
        roles = self.get_all()
        for role in roles:
            if role.category == category:
                record.append(role)
        return record

    def get_role_by_tag(self, tag: str) -> list[Role]:
        record = []
        roles = self.get_all()
        for role in roles:
            if role.tag == tag:
                record.append(role)
        return record

# 建立唯一實例
role_manager = RoleManager()
