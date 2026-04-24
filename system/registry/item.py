from game import model

from cores.registry import AssetRegistry

class ItemReigstry(AssetRegistry[model.Item]):
    def __init__(self):
        super().__init__(
            model = model.Item, 
            path = "assets/items"
        )

# singleton declaration.
item_registry = ItemReigstry()
