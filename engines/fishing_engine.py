import random
from utils.logger import logger
from context import Context
from database.inventory import Inventory
from database.skill import Skill

class FishingEngine:
    def cast(self, interaction):
        player_id = interaction.user.id
        
        # 抽取物品
        payload = self.roll()
        
        # 更新數據庫
        for item in payload:
            logger.debug(f"玩家 {player_id} 獲得物品 {item['item_id']} x{item['quantity']}，經驗值 {item['experience']}")
            Inventory.add_item(player_id, item['item_id'], item['quantity'])
            Skill.add_experience(player_id, item['experience'], "fishing")
        
        return payload

    def roll(self):
        loot_table = Context.json_loader.load("loot_table/fishing.json")
        pool = loot_table.get("default_pool")

        payload = []

        for item in pool:
            if item.get("chance") > random.random():
                item_id = item.get("item_id")
                quantity = 1
                experience = item.get("experience")

                payload.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "experience": experience
                })

        return payload