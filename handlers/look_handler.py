from context import Context

import random

class LookHandler:
    def __init__(self):
        print("[LookHandler] Handler loaded.")

    def draw_entity(self, ) -> list[dict[str, any]]:
        entity_container = Context.get_container("entity") 
        entities = entity_container.get_all() # get entity dict with { ID/str : Entity/object }

        found_entities = []
        for _ in range(random.randint(3, 5)):
            e = random.choice(list(entities.values()))
            found_entities.append({"image": e.image, "name": e.name, "level": e.level}) 

        return found_entities