"""
這個類別用來管理商店邏輯，包含讀取商品列表、驗證商品、回傳商品清單 (options) 等功能。
"""

import discord
import json
from models.item import item_manager

class Shop:
    def __init__(self, shop_name: str):
        self.shop_name = shop_name
        self.items = {}
        self.load(shop_name)

    def load(self, shop_name: str):
        with open(f"data/shop/{shop_name}.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                item_id = item.get("item_id")
                if item_id:
                    item_ = item_manager.get_item(item_id)
                    self.items[item_id] = {**item, **item_} # 合併字典

    def get_options(self):
        options = []
        for item_id, data in self.items.items():
            option = discord.SelectOption(
                value=item_id,
                label=f"{data.get('item_name')}, 費用： {data.get('price')} 金幣", 
                emoji=data.get('emoji'),
                description=data.get("description"), 
                )
            options.append(option)
        
        return options
    
    def get_item(self, item_id: str) -> dict:
        # 這個方法取得的物品會包含價格等商店資訊
        return self.items.get(item_id)