class Inventory:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.items = {}

    def add_item(self, item_id: str, quantity: int = 1):
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity
    
    def remove_item(self, item_id: str, quantity: int = 1) -> dict:
        if item_id not in self.items or self.items[item_id] < quantity:
            return {
                'success': False,
                'remaining': self.items.get(item_id, 0),
                'message': f'數量不足，該物品僅有 {self.items.get(item_id, 0)} 個）'
            }
        
        self.items[item_id] -= quantity
        return {
            'success': True,
            'remaining': self.items[item_id],
            'message': f'成功扣除 {quantity} 個 {item_id}'
        }