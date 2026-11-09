from lib import player
from lib import item
from lib.item import equip_sort_key

from model import Player
from model import ItemInstance

Player.get_or_create(id=1)

# 打亂獲得物品的順序
item.give(1, "leather_hat", 1)
item.give(1, "rough_fishing_rod", 1)

# 打亂裝備的順序
success, msg = player.equip(1, "leather_hat", "head")
print(success, msg)
success, msg = player.equip(1, "rough_fishing_rod", "main_hand")
print(success, msg)

# 取得所有已裝備物品
rows = player.get_equipments(player=1, unequipped=False)

for row in rows:
    print(row.item_id, row.slot)

rows.sort(key=equip_sort_key)

for row in rows:
    print(row.item_id, row.slot)