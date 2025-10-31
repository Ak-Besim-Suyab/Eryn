from context import Context

import random

class LookHandler:
    def __init__(self):
        print("[LookHandler] Handler loaded.")

    def draw_target(self, player) -> list[dict[str, any]]:
        # target condition: area, weather(not implement), time(not implement), quest(not implement)
        spawner = Context.loader.load(f"assets/spawners/{player.location}")
        spawner_pool = spawner.get("pool") 

        # entity dict will be: { uid str : Entity() object }
        entity_container = Context.get_container("entity") 
        entities = entity_container.get_all() 

        found_entities = []
        for entry in spawner_pool:
            entity = entities.get(entry.get("uid"))
            found_entities.append(entity.to_dict()) 

        return found_entities