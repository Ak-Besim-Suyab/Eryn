"""
這個檔案負責定義資源 (Resource) 以及資源管理器 (ResourceManager)
資源 (Resource) 是地圖使用探索指令後會顯現的可互動物件，互動方式取決於資源要求的技能 (例如：白樺樹需要砍伐技能 Lv.1 以上)
預計會將樹木、礦石、建築等非生物物件定義為資源 (Resource)
資源會包含掉落表 (drops) 調用時請使用物品管理器 (ItemManager) 檢驗與發送掉落物
"""
import random
from collections import Counter
from dataclasses import dataclass, field
from cores.manager import Manager
from cores.logger import logger

from models.loot import loot_manager

# 這個物件定義掉落物列表
@dataclass
class Drop:
    id: str
    weight: int

@dataclass
class Resource:
    id: str
    name: str
    min: int = 1
    max: int = 1
    drops: list[Drop] = field(default_factory=list)

    def __post_init__(self):
        # 這裡是後處理，把宣告後的物件裡的掉落表 (loots) 轉換成 Loots 類別的實例，然後再放回去
        if self.drops and isinstance(self.drops[0], dict):
            self.drops = [Drop(**drop) for drop in self.drops]

    def roll(self) -> dict[str, int]:
        if not self.drops:
            return {}
        
        weights = [drop.weight for drop in self.drops]
        if sum(weights) == 0:
            return {}
        
        result = Counter()
        record = random.choices(self.drops, weights=weights, k=1)[0]
        random_time = random.randint(self.min, self.max)
        for count in range(random_time):
            logger.debug(f"進入抽取, 掉落表: {self.name}, 戰利品表: {record.id}, 當前次數: {count + 1}")
            result.update(loot_manager.roll(record.id))

        return dict(result)

class ResourceManager(Manager[Resource]):
    def __init__(self):
        super().__init__(
            model = Resource, 
            path = "assets/resources"
        )

# 建立唯一實例
resource_manager = ResourceManager()
