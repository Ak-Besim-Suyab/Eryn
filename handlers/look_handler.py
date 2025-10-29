from context import Context

import random

class LookHandler:
    def __init__(self):
        print("[LookHandler] Handler loaded.")

    def draw_target(self, player) -> list[dict[str, any]]:
        spawner = Context.loader.load(f"assets/spawners/{player.location}")
        spawner_pool = spawner.get("pool") 

        # get entity dict { entity_id str : Entity() object }
        entity_container = Context.get_container("entity") 
        entities = entity_container.get_all() 

        found_entities = []
        for entry in spawner_pool:
            entity = entities.get(entry.get("entity_id"))
            found_entities.append(
                { 
                    "entity_id":entity.uid,
                    "entity_name": entity.name,
                    "level": entity.level,
                    "image": entity.image
                }
            ) 

        return found_entities