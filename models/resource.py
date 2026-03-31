"""
這個檔案負責定義資源 (Resource) 以及資源管理器 (ResourceManager)
資源 (Resource) 是地圖使用探索指令後會顯現的可互動物件，互動方式取決於資源要求的技能 (例如：白樺樹需要砍伐技能 Lv.1 以上)
預計會將樹木、礦石、建築等非生物物件定義為資源 (Resource)
資源會包含掉落表 (drops) 調用時請使用物品管理器 (ItemManager) 檢驗與發送掉落物
"""

from dataclasses import dataclass
from cores.loader import JsonLoader
from cores.logger import logger

resource_path = "assets/resources"


@dataclass
class Resource:
    id: str
    name: str
    drops: list[str] = None


class ResourceManager:
    def __init__(self):
        self._resources: dict[str, Resource] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(resource_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"ResourceManager | 找不到資料夾: {resource_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"ResourceManager | {filename} 的 JSON 格式錯誤")
                continue
            
            try:
                resource = Resource(**data)
                self._resources[resource.id] = resource
                total_files += 1
                logger.info(f"ResourceManager | 載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"ResourceManager | {filename} 的 JSON 格式與 Resource 類別不相容: {e}")
                continue
        
        logger.info(f"ResourceManager | 資料載入完畢，總共載入 {total_files} 個檔案")

    def get_resource(self, resource_id: str) -> Resource | None:
        return self._resources.get(resource_id)

    def get_all_resources(self) -> list[Resource]:
        return list(self._resources.values())

# 建立唯一實例
resource_manager = ResourceManager()
