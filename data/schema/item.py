from dataclasses import dataclass, field

class ComponentMap:
    def __init__(self, data: dict):
        self._data = data # {ItemComponent: values}

    def get(self, type, default=None):
        return self._data.get(type, default)

    def has(self, type) -> bool:
        return type in self._data

@dataclass
class Item:
    """
    .. sort::
        排序用浮點數
    """
    id: str
    serial: float    = 9999.9
    name: str        = "未知物品"
    description: str = "沒有任何描述"
    tooltip: str     = "無"
    icon: str        = "📦"

    tags: list[str] | None   = field(default_factory=list)
    components: ComponentMap = field(default_factory=lambda: ComponentMap({}))

    def has_tags(self, *tags) -> bool:
        return set(tags).issubset(self.tags)

    def get(self, type, default=None):
        return self.components.get(type, default)

    def has(self, type) -> bool:
        return self.components.has(type)