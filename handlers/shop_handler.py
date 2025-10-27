from asset_manager import asset_manager

class ShopHandler:
    def __init__(self):
        self.item_list = asset_manager.get_asset("items")
        print("shop handler initialized.")

    def buy_item(self, player, item_id: str, amount=1):
        
        price = self.item_list[item_id]["base_value"] * amount

        if player.gold < price:
            return "💸 金幣不足，無法購買！"

        player.gold -= price
        player.inventory.add_item(item_id, amount)
        player.save_player()

        print(f"[ShopHandler] Purchasing {item_id} success.")
        #return f"✅ 成功購買 **{item_id}**！花費 {price} 金幣"

shop_handler = ShopHandler() #unique object