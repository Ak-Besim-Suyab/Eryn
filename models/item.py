from context import Context

class Item:
    def __init__(self, uid: str, name: str, image="❓"):
        self.uid = uid
        self.name = name
        self.image = image

        print(f"[Item] Item {self.uid} registered.")

    def __repr__(self):
        return f"<Item {self.name} {self.uid}>"

class ItemContainer:
    def __init__(self):
        self.items: dict[str, Item] = {}

    def register(self):
        file_loader = Context.file_loader
        # item registry.
        self.items["mudstone"] = Item(uid="mudstone", name="泥岩", image=file_loader.load("textures/mudstone").get("image"))
        self.items["slate"] = Item(uid="slate", name="板岩", image=file_loader.load("textures/slate").get("image"))
        self.items["metal_ore"] = Item(uid="metal_ore", name="金屬碎塊", image=file_loader.load("textures/metal_ore").get("image"))
        self.items["antique_silver_coin"] = Item(uid="antique_silver_coin", name="舊銀幣", image=file_loader.load("textures/antique_silver_coin").get("image"))

        print("[ItemContainer] Container loaded.")

    def get_item(self, uid: str) -> Item | None:
        return self.items.get(uid)

    def get_all(self) -> dict:
        return self.items