from context import Context

class Inventory:
    def __init__(self, ID: int):
        self.ID = ID
        self.items = {}

    def has_item(self, item_id: str):
        return self.items.get(item_id) if self.items.get(item_id) else 0

    def set_item(self, item_id: str, quantity: int):
        self.items[item_id] = quantity

    def add_item(self, item_id: str, quantity: int):
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id: str, quantity: int):
        if item_id in self.items and self.items[item_id] >= quantity:
            self.items[item_id] -= quantity
            if self.items[item_id] == 0:
                del self.items[item_id]
        else:
            print("[Inventory] Not enough quantity in inventory, please check code.")