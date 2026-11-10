from model import Inventory
from model import ItemInstance

# 如何查詢指定道具然後刪除所有符合名稱的道具, 如果只要刪除特定玩家, where 加上玩家條件即可
# deleted = (Inventory
#            .delete()
#            .where(Inventory.item_id == "iron_crate")
#            .execute())

# print(f"已刪除 {deleted} 筆")

# deleted = (Inventory
#            .delete()
#            .where(Inventory.item_id == "wood_crate",
#                   Inventory.player == 1)
#            .execute())

# print(f"已刪除 {deleted} 筆")

deleted = (ItemInstance
           .delete()
           .where(ItemInstance.item_id == "hazel_fishing_rod")
           .execute())

# 怎麼找到某個未穿戴的裝備, 然後只刪掉一筆, 查詢條件還能再增加
# instance = (ItemInstance
#             .select()
#             .where(
#                 ItemInstance.item_id == "admin_fishing_rod", # 查詢指定裝備名稱
#                 ItemInstance.player == 1, # 查詢指定玩家
#                 ItemInstance.slot.is_null(True) # 查詢 slot 為空的裝備
#             )
#             .order_by(ItemInstance.id) # 依照 id 排序
#             .first()) # 找到第一筆

# print(instance.item_id)

# deleted = (ItemInstance
#            .delete()
#            .where(
#                ItemInstance.id == instance.id,
#            )
#            .execute())

# print(f"已刪除 {deleted} 筆")