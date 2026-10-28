from . import item
from . import resource

def _give_item(player_id):     item.give(player_id)
def _give_resource(player_id): resource.give(player_id)

REWARD_HANDLERS = {
    "item": item.give,
    "resource": resource.give,
}