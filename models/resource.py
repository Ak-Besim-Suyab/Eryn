"""
這個檔案負責定義資源 (Resource) 以及資源管理器 (ResourceManager)
資源 (Resource) 是地圖使用探索指令後會顯現的可互動物件，互動方式取決於資源要求的技能 (例如：白樺樹需要砍伐技能 Lv.1 以上)
預計會將樹木、礦石、建築等非生物物件定義為資源 (Resource)
資源會包含掉落表 (drops) 調用時請使用物品管理器 (ItemManager) 檢驗與發送掉落物
"""
import random
from dataclasses import dataclass, field
from cores.loader import JsonLoader
from cores.logger import logger

from models.loot import loot_manager

resource_path = "assets/resources"


# 這個物件定義掉落物列表
@dataclass
class Drop:
    id: str
    weight: int


@dataclass
class Resource:
    id: str
    name: str
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
        
        record = random.choices(self.drops, weights=weights, k=1)[0]

        return loot_manager.roll(record.id)
        

class ResourceManager:
    def __init__(self):
        self._resources: dict[str, Resource] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(resource_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"找不到資料夾: {resource_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"{filename} 的 JSON 格式出現錯誤")
                continue
            
            try:
                resource = Resource(**data)
                self._resources[resource.id] = resource
                total_files += 1
                logger.info(f"載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"{filename} 的 JSON 格式與 Resource 類別不相容: {e}")
                continue
        
        logger.info(f"資料載入完畢，總共載入 {total_files} 個檔案")

    def get_resource(self, resource_id: str) -> Resource | None:
        return self._resources.get(resource_id)

    def get_all_resources(self) -> list[Resource]:
        return list(self._resources.values())

# 建立唯一實例
resource_manager = ResourceManager()
