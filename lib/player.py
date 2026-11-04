from cores import logger
from cores.database import database

from models import Player, ItemInstance

from lib import item as itemlib
from lib import resource as reslib

from data import RESOURCES, LOOT_TABLES, ITEMS
from data.schema.type import ItemType
from data.schema import Item

def equip(player_id: int, item_id: str, slot: str) -> tuple[bool, str]:
    """ 
    裝備物品到指定欄位, 返回是否成功更改紀錄與對應輸出訊息
    """
    #NOTE: 這裡有個問題, 是否會搜尋到名稱相同的裝備? 需要處理
    instance = ItemInstance.get_or_none(ItemInstance.player == player_id, ItemInstance.item_id == item_id)

    # 沒有任何裝備存在
    if instance is None:
        return False, "找不到物品"

    # 物品已被裝備
    if instance.slot is not None:
        return False, "物品已裝備"

    item = ITEMS.get(item_id)
    component = item.get_component(ItemType.EQUIPMENT) if item else None

    # 沒有可裝備的標籤, 或該物品被定位成不可裝備
    if component is None or component.slot is None:
        return False, "物品無法裝備"

    # 物品槽位與指定槽位不符
    #NOTE: 之後在選取時可能就會直接過濾掉不可裝備的欄位, 目前保留檢查
    if slot != component.slot:
        return False, "物品無法裝備到該欄位"

    with database.atomic():
        # 尋找可裝備的物品
        instance = (ItemInstance
                    .select()
                    .where(ItemInstance.player == player_id,
                           ItemInstance.item_id == item_id,
                           ItemInstance.slot.is_null(True))
                    .order_by(ItemInstance.id)
                    .first())
        if instance is None:
            return False, "找不到可裝備的物品"
        
        # 卸下舊裝備
        (ItemInstance
        .update(slot=None)
        .where(ItemInstance.player == player_id, ItemInstance.slot == slot)
        .execute())

        # 穿上裝備
        (ItemInstance
        .update(slot=slot)
        .where(ItemInstance.id == instance.id)
        .execute())

    return True, "成功裝備"

def unequip(player_id: int, slot: str) -> bool:
    """ 移除指定欄位的物品，返回是否成功移除該筆紀錄
    """
    with database.atomic():
        deleted = (ItemInstance
                   .update(slot=None)
                   .where(
                       ItemInstance.player == player_id, 
                       ItemInstance.slot == slot, 
                       ItemInstance.slot.is_null(False))
                    .execute())

    return deleted > 0

def open_item(player_id: int, item: Item, times: int = 1) -> tuple[bool, dict]:

    loot = item.get_component(ItemType.LOOT)
    if loot is None:
        return False, None

    # NOTE: 這裡先實作簡易邏輯，之後如果讓 loot_table 可以有多個，則需要再做調整
    loot_table = LOOT_TABLES.get(loot.loot_tables[0])
    if loot_table is None:
        logger.warning(f"找不到物品 {item.id} 的掉落表 {loot.loot_tables[0]}")
        return False, None

    looted = loot_table.roll(times)

    item_lines = []
    for (loot_type, loot_id), quantity in looted.items():
        match loot_type:
            case "resource":
                res = RESOURCES.get(loot_id)
                reslib.give(player_id, loot_id, quantity)
                # NOTE: 這裡之後改成 description.append(resource.get_line(item_id, quantity))
                item_lines.append(f"- {res.icon}{res.name} {quantity}")
            case _:
                pass

    itemlib.remove(player_id, item.id, times)

    return True, item_lines

def get_timestamp_daily(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_daily

def set_timestamp_daily(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_daily = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的每日時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的每日時間戳記")

def get_timestamp_voice(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_voice

def set_timestamp_voice(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_voice = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的語音時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的語音時間戳記")