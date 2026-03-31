"""
這個檔案負責定義地區 (Region) 以及地區管理器 (RegionManager)
"""

from dataclasses import dataclass
from cores.loader import JsonLoader
from cores.logger import logger

region_path = "assets/regions"


@dataclass
class Region:
    id: str
    name: str
    resources: list[str] = None


class RegionManager:
    def __init__(self):
        self._regions: dict[str, Region] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(region_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"RegionManager | 找不到資料夾: {region_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"RegionManager | {filename} 的 JSON 格式錯誤")
                continue
            
            try:
                region = Region(**data)
                self._regions[region.id] = region
                total_files += 1
                logger.info(f"RegionManager | 載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"RegionManager | {filename} 的 JSON 格式與 Region 類別不相容: {e}")
                continue
        
        logger.info(f"RegionManager | 資料載入完畢，總共載入 {total_files} 個檔案")

    def get_region(self, region_id: str) -> Region | None:
        return self._regions.get(region_id)
    
    def get_all_regions(self) -> list[Region]:
        return list(self._regions.values())

# 建立唯一實例
region_manager = RegionManager()
