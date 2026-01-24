import random
from utils.logger import logger
from context import Context
from database.inventory import Inventory
from database.skill import Skill
from database.player import Player

TREASURE_CHANCE = 0.1

class FishingEngine:
    def cast(self, interaction):
        player_id = interaction.user.id
        
        # roll items
        result = self.roll()
        
        # update database
        for item in result:
            if item.get("event_type") == "general":
                Inventory.add_item(player_id, item['item_id'], item['quantity'])
                Skill.add_experience(player_id, item['experience'], "fishing")
            elif item.get("event_type") == "treasure":
                Player.increase_currency(player_id, item['currency'])

        return result

    def roll(self, loop: int =1):
        loot_table = Context.json_loader.load("loot_table/fishing.json")
        pool = loot_table.get("default_pool")

        result = []

        # general roll.
        for _ in range(loop):
            item = random.choice(pool)
            if item.get("chance") > random.random():
                item_id = item.get("item_id")
                quantity = 1
                experience = item.get("experience")

                result.append(
                    {
                        "event_type": "general",
                        "item_id": item_id,
                        "quantity": quantity,
                        "experience": experience
                    }
                )
        
        # additional roll for treasure event.
        # result must not be empty.
        if result and random.random() < TREASURE_CHANCE:
            bonus_currency = random.randint(5, 10)
            result.append(
                {
                    "event_type": "treasure",
                    "currency": bonus_currency
                }
            )

        return result