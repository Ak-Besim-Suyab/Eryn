from context import Context

class Item:
    def __init__(self, item_id: str, name: str, image="❓"):
        self.item_id = item_id
        self.name = name
        self.image = image

        print(f"[Item] Item {self.item_id} registered.")

    def __repr__(self):
        return f"<Item {self.name} {self.item_id}>"

class ItemContainer:
    def __init__(self):
        self.items: dict[str, Item] = {}

    def register(self):
        loader = Context.loader
        # item registry.
        self.items["mudstone"] = Item(item_id="mudstone", name="泥岩", image=loader.load("textures/mudstone").get("image"))
        self.items["slate"] = Item(item_id="slate", name="板岩", image=loader.load("textures/slate").get("image"))
        self.items["metal_ore"] = Item(item_id="metal_ore", name="金屬碎塊", image=loader.load("textures/metal_ore").get("image"))
        self.items["antique_silver_coin"] = Item(item_id="antique_silver_coin", name="舊銀幣", image=loader.load("textures/antique_silver_coin").get("image"))

        print("[ItemContainer] Container loaded.")

    def get_item(self, item_id: str) -> Item | None:
        return self.items.get(item_id)

    def get_all(self) -> dict:
        return self.items