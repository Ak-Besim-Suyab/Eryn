from dataclasses import dataclass
from cores.registry import Registry

@dataclass
class Shop:
    item_list: list = None


class ShopManager(Registry[Shop]):
    def __init__(self):
        super().__init__(
            model = Shop, 
            path = "game/shops/assets"
        )

shop_manager = ShopManager()