import discord
import random

from context import Context

TREASURE_CHANCE = 0.1

class FishingEngine:
    def __init__(self):
        self.loot_table = Context.json_loader.load("loot_table/fishing.json")

    def cast(self, loop: int =1):
        pool = self.loot_table.get("default_pool")

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