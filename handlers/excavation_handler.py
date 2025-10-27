import random

from context import Context

class ExcavationHandler:
    def __init__(self):
        print("[ExcavationHandler] Handler loaded.")

    def draw(self, player) -> list:
        table = Context.loader.load("loot_table/excavation_loot")
        pool = table.get(player.location).get("pool")

        item_registry = Context.get_container("item").get_all()

        result=[]
        for loot in pool:
            if loot.get("chance") > random.random():
                looted_item = item_registry[loot.get("item_id")]
                looted_quantity = random.randint(1, 5)
                result.append(
                    { 
                        "item_id": looted_item.ID,
                        "name": looted_item.name,
                        "image": looted_item.image,
                        "quantity": looted_quantity
                    }
                )

        return result

    def draw_experience(self) -> list:
        result = [
            {"skill_id": "character", "experience": random.randint(500, 800)}, 
            {"skill_id": "excavation", "experience": random.randint(750, 1200)}
        ]

        return result