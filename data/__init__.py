from .registry import (
    SKILLS,
    REGIONS,
    ITEMS,
    SLOTS,
    MATERIALS,
    CONTAINERS, 
    ROLES,
    LOOT_TABLES,
    LINES,
    RACES,
)

# 告訴所有導入此模組的函式庫該模組包含哪些函式庫
__all__ = [
    "SKILLS",
    "REGIONS",
    "ITEMS",
    "SLOTS",
    "MATERIALS",
    "CONTAINERS",
    "ROLES",
    "LOOT_TABLES",
    "LINES",
    "RACES",
]

# 用法: 
# from data imort DATA_OBJECT
# data = DATA_OBJECT.get(name)