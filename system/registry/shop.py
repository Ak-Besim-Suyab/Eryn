from cores.registry import AssetRegistry

from game.model import Shop

class ShopRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(path = "assets/shops")

    def get(self, shop_id: str):
        data = self._data.get(shop_id)
        if not data:
            return None
        return Shop(**data)

# singleton declaration.
shop_registry = ShopRegistry()