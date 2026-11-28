"""
測試 player.equip(), player.unequip() 裝備函式
"""
from lib import player
from models import Player
from data import ITEMS
from data.schema.item_component import EQUIPMENT

# 取得裝備
_item = ITEMS.get("rough_fishing_rod")

# 查看詞綴與裝備欄位
component = _item.get(EQUIPMENT)
if component:
    print(component.slot)
    print(component.affixes)

# 模擬物件
Player.get_or_create(id=1)

# 測試 equip() function
success, msg = player.equip(1, "wooden_fishing_rod", "main_hand")

# 找不到物品時, 理論輸出 False, "找不到物品"
# 已有裝備時, 理論輸出 False, "物品已裝備"
# 無法裝備時, 理論輸出 False, "物品無法裝備"
# 無法裝備到該欄位時, 理論輸出 False, "物品無法裝備到該欄位"
# 裝備成功時, 理論輸出 True, "成功裝備"
print(success, msg)

# 測試 unequip() function
success = player.unequip(1, "main_hand")

# 移除失敗時, 理論輸出 False
# 移除成功時, 理論輸出 True
print(success)