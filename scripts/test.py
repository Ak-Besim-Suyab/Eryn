from data import ITEMS, SLOTS
from lib import player, item
slot = SLOTS.get("head")
print(slot)

i = ITEMS.get("leather_hat")
print(i)

item.give(1184440057596235817, "leather_hat", 1)

success, msg = player.equip(1184440057596235817, "leather_hat", "head")
print(success, msg)

lst = player.get_equipments(player_id=1184440057596235817)
for i in lst:
    print(i.slot)