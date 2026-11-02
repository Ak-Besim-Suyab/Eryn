from .registry import (
    ITEMS,
    RESOURCES,
    CONTAINERS, 
    ROLES,
    BUILDINGS,
    LOOT_TABLES,
    LINES,
)

# 告訴所有導入此模組的函式庫該模組包含哪些函式庫

__all__ = [
    "ITEMS",
    "RESOURCES",
    "CONTAINERS",
    "ROLES",
    "BUILDINGS",
    "LOOT_TABLES",
    "LINES",
]

# 用法: 
# from data imort DATA_OBJECT
# data = DATA_OBJECT.get(name)