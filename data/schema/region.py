"""
地圖資料物件
id  : 地圖識別碼
name: 地圖顯示名稱
"""
from dataclasses import dataclass

@dataclass
class Region:
    id: str
    name: str