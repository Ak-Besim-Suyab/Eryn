from dataclasses import dataclass, field

# 裝備欄位與對應名稱
SLOT_CACHES = {
    "main_hand": "主手",
    "off_hand" : "副手",
    "ammo"     : "彈藥",
    "head"     : "頭"  ,
    "body"     : "身體",
    "arms"     : "手"  ,
    "belt"     : "腰帶",
    "legs"     : "腿"  ,
    "feet"     : "腳"  ,
    "earring"  : "耳環",
    "necklace" : "項鍊",
    "ring"     : "戒指",
    None       : "無",
}

@dataclass
class Race:
    id: str
    name: str
    slots: list[str] = field(default_factory=list)

#NOTE: Race 只知道他有什麼初始裝備欄位, 欄位的其他具體行為則從邏輯裡獲取