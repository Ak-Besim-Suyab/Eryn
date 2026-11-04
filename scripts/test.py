from lib import player, item
from lib.stat import get_stats

item.give(1, "hazel_fishing_rod", 1)

player.equip(1, "hazel_fishing_rod", "main_hand")

stat = get_stats(1)
print(stat.get("fishing", "luck"))