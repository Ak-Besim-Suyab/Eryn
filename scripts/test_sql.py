from models import Inventory

deleted = (Inventory
           .delete()
           .where(Inventory.item_id == "iron_crate")
           .execute())

print(f"已刪除 {deleted} 筆")

deleted = (Inventory
           .delete()
           .where(Inventory.item_id == "wood_crate")
           .execute())

print(f"已刪除 {deleted} 筆")

deleted = (Inventory
           .delete()
           .where(Inventory.item_id == "rose_yellow")
           .execute())

print(f"已刪除 {deleted} 筆")