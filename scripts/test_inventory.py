"""
測試背包函式
"""
from lib import item, inventory
from models import Inventory, ItemInstance

# 嘗試在背包加入道具
# entry, _ = Inventory.get_or_create(player=1, item_id="wooden_crate", defaults={"quantity": 0})

# (Inventory
#     .update(quantity = Inventory.quantity + 1)
#     .where(Inventory.id == entry.id)
#     .execute())

# 嘗試在背包加入裝備
# ItemInstance.create(player=1, item_id="wooden_fishing_rod")

# 取得指定頁面的物品列表, 頁數, 總頁數
# rows, page, total_pages = inventory.get_page(1, 1, None)

# 印出字串
# lines = []
# for row in rows:
#     if isinstance(row, ItemInstance):
#         lines.append(item.summary_line(row.item_id, 1))
#     else:
#         lines.append(item.summary_line(row.item_id, row.quantity))

# 輸出格式化字串後的物品列表
# print("\n".join(lines))

# 測試是否可以透過資料庫 id 欄位取得指定物品, 而非所有符合外部條件的物品列表
i = ItemInstance.get_or_none(
    ItemInstance.player == 1, 
    ItemInstance.id == 18,
    ItemInstance.item_id == "wooden_fishing_rod"
    )
if i:
    print(i.id, i.item_id, i.slot)
else:
    print("Item not found.")