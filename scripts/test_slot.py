# 起始有預設裝備欄位表 (根據種族改變)
# 後續判定時會查詢其他特性並將額外的欄位合併進去

from data import RACES
from data.schema import Race

from model import Player

from lib import player

default = [
    "hand:1",
    "hand:2",

    "head:1",
    "glove:1",
    "body:1",
    "leg:1",
    "feet:1",

]

max_slots = [
    "hand_1",
    "hand_2",
    "hand_3",
    "hand_4",

    "head_1",
    "head_2",
    "head_3",

    "body",

    "leg",

    "feet_1",
    "feet_2",
    "feet_3",
    "feet_4",

    "earring_1",
    "earring_2",
    "earring_3",
    "earring_4",

    "ring_1",
    "ring_2",
    "ring_3",
    "ring_4",
]

p, _ = Player.get_or_create(id=1)
print(p.race)
# race = RACES.get(p.race)

# for slot in race.equip_slots:
#     print(slot)

# 邏輯
#
# 裝備只指示部位, 例如: head
# 
# 存檔時以資料庫 ID 作為分割值保存, 例如:
#
# 裝備的 ID 是 26, 部位是 head, 最後存在資料庫的 slot 會是 head:26
# 解決多個部位的唯一鍵問題
#
# 進入系統時, 系統會先統計玩家屬性總共能戴多少頭盔, 然後歷遍已裝備的頭盔有幾個