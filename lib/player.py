from cores import logger

from models import Player, ItemInstance

from lib import item as itemlib
from lib import resource as reslib

from data import RESOURCES, LOOT_TABLES, ITEMS
from data.schema import ActionType

from data.schema import Item

def equip(player_id: int, item_id: str, slot: str):

    item = ITEMS.get(item_id)

    update = (ItemInstance
              .update())

def open_item(player_id: int, item: Item, times: int = 1) -> tuple[bool, dict]:

    loot = item.get_component(ActionType.LOOT)
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