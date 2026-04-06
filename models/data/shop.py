from dataclasses import dataclass
from cores.manager import Manager

@dataclass
class Shop:
    """
    這個是商店的資料類別
    """
    id: str
    item_list: list = None


class ShopManager(Manager[Shop]):
    """
    這個是商店的資料類別管理器，有唯一實例。
    """
    def __init__(self):
        super().__init__(
            model = Shop, 
            path = "assets/shops"
        )

shop_manager = ShopManager()