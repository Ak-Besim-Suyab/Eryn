from .registry import (
    ITEMS,
    SLOTS,
    RESOURCES,
    CONTAINERS, 
    ROLES,
    BUILDINGS,
    LOOT_TABLES,
    LINES,
    RACES,
)

# 告訴所有導入此模組的函式庫該模組包含哪些函式庫
__all__ = [
    "ITEMS",
    "SLOTS",
    "RESOURCES",
    "CONTAINERS",
    "ROLES",
    "BUILDINGS",
    "LOOT_TABLES",
    "LINES",
    "RACES",
]

# 用法: 
# from data imort DATA_OBJECT
# data = DATA_OBJECT.get(name)