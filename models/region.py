from dataclasses import dataclass
from cores.manager import Manager

@dataclass
class Region:
    """
    這個是地圖的資料類別
    """
    id: str
    name: str
    resources: list[str] = None


class RegionManager(Manager[Region]):
    """
    這個是地圖的資料類別管理器，有唯一實例。
    """
    def __init__(self):
        super().__init__(
            model = Region, 
            path = "assets/regions"
        )

region_manager = RegionManager()
