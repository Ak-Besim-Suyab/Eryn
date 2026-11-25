"""
地圖資料物件
id          : 地圖識別碼
name        : 地圖顯示名稱
description : 地圖描述
cost        : 移動到其他位置的花費
loot_table  : 各技能對應的戰利品表名稱
role_id     : 移動到該地區時給予的 Discord 身分組 ID
"""
from dataclasses import dataclass, field

@dataclass
class Region:
    id: str
    name: str
    description: str
    cost: dict
    loot_table: dict[str, str] = field(default_factory=dict)
    role_id: int | None = None