"""
這個函式庫用於蒐集玩家的所有可加總屬性，並集合成一個狀態物件提供給其他系統存取。
"""
from collections import defaultdict

from data import ITEMS
from data.schema import Affix
from data.schema.type import ItemType

from model import ItemInstance

def _collect(player_id: int) -> list[Affix]:
    """
    返回指定玩家身上所有已穿戴裝備固有與額外取得的`Affix`屬性物件列表
    """
    # 查詢所有已穿戴裝備
    equipped = (ItemInstance
                .select()
                .where(ItemInstance.player == player_id, 
                       ItemInstance.slot.is_null(False))) 

    # 擷取所有裝備屬性
    collections = []
    for inst in equipped:
        item = ITEMS.get(inst.item_id)
        comp = item.get_component(ItemType.EQUIPMENT) if item else None
        
        # 裝備固有屬性，本身就是 Affix 物件，直接加入列表
        if comp:
            collections.extend(comp.affixes)

        # 來自隨機取得的額外屬性，需要先宣告為 Affix 物件再加入列表
        for a in inst.affixes:
            collections.append(Affix(scope=a.scope, stat=a.stat, operator=a.operator, value=a.value))

    return collections

class Stats:
    def __init__(self, affixes: list[Affix]):
        self._add      = defaultdict(float)
        self._increase = defaultdict(float)
        self._more     = defaultdict(lambda: 1.0)
        for a in affixes:
            key = (a.scope, a.stat)
            match a.operator:
                case "add":      self._add[key] += a.value
                case "increase": self._increase[key] += a.value
                case "more":     self._more[key] += a.value

    def get(self, scope: str, stat: str, base: float = 0.0) -> float:
        """
        返回統計並計算後的屬性值，公式：`(base + add) * (1 + increase) * more`
        """
        key = (scope, stat)
        return (base + self._add[key]) * (1 + self._increase[key]) * self._more[key]

def get_stats(player_id: int) -> Stats:
    """
    返回指定玩家的裝備屬性加總物件
    """
    return Stats(_collect(player_id))