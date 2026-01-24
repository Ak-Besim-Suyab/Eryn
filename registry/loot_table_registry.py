from managers.loot_table_manager import LootTableManager

loot_table_manager = LootTableManager()

# 註冊所有掉落表（直接使用檔案路徑以字典形式載入）
loot_table_manager.register("fishing", "loot_table/fishing.json")
