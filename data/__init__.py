from .registry import (
    container, 
    item,
    role
)

# 告訴所有導入此模組的函式庫該模組包含哪些函式庫

__all__ = [
    "container",
    "item",
    "role"
]

#
# 用法: 
# import data
# data = data.item.get(name)
#