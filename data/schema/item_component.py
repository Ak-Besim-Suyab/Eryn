from dataclasses import dataclass

@dataclass(frozen=True)
class Food:
    saturation: float = 0.0

@dataclass(frozen=True)
class Affix:
    scope: str
    stat: str
    value: int | float
    operator: str = "add"

@dataclass(frozen=True)
class Equipment:
    slot: str | None = None
    affixes: tuple[Affix, ...] = ()

@dataclass(frozen=True)
class Loot:
    loot_tables: tuple[str, ...] = ()

# -------------------------------------------------------

class ItemComponent:
    def __init__(self, name: str, component):
        self.name = name
        self.component = component

    def __deepcopy__(self, memo):
        # 元件識別鍵採單例語意，避免 deepcopy 後無法在 ComponentMap 中匹配
        return self

    def __repr__(self):
        return f"<ItemComponent `{self.name}`>"

COMPONENTS: dict[str, ItemComponent] = {}

def create(name: str, component) -> ItemComponent:
    COMPONENTS[name] = ItemComponent(name, component)
    return COMPONENTS[name]

FOOD      = create("food",      lambda raw: Food(**raw))
LOOT      = create("loot",      lambda raw: Loot(loot_tables=tuple(raw.get("loot_tables") or [])))
EQUIPMENT = create("equipment", lambda raw: Equipment(slot=raw.get("slot"), affixes=tuple(Affix(**a) for a in (raw.get("affixes") or []))))
AFFIX     = create("affix",     lambda raw: Affix(**raw))