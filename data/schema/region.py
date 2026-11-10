"""
地圖資料物件
id  : 地圖識別碼
name: 地圖顯示名稱
description: 地圖描述
cost: 移動到其他位置的花費
"""
from dataclasses import dataclass

@dataclass
class Region:
    id: str
    name: str
    description: str
    cost: dict