from game import model

from cores.registry import AssetRegistry

class ShopRegistry(AssetRegistry[model.Shop]):
    def __init__(self):
        super().__init__(
            model = model.Shop, 
            path = "assets/shops"
        )

# singleton declaration.
shop_registry = ShopRegistry()