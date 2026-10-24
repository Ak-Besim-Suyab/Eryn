import data

from cores import logger
from cores import database

from models import Player, Inventory

def give_item(player_id: int, item_id: str, amount: int = 1) -> int:
    
    """給予玩家物品，回傳給予後的持有數量
    """
    if amount <= 0:
        raise ValueError("增加物品的數量必須大於 0")

    # TODO: 與 remove_item 有共用片段, 之後將這段檢查取出
    item = data.item.get(item_id)
    if item is None:
        logger.debug(f"錯誤，物品不存在或名稱錯誤: {item_id}")
        return
    if amount <= 0:
        logger.debug(f"錯誤，數量必須為正整數: {amount}")
        return
        
    Player.get_or_create(id=player_id)

    with database.atomic():
        entry, _ = Inventory.get_or_create(player = player_id, item_id = item_id, defaults = {"quantity": 0})
        
        (Inventory
            .update(quantity = Inventory.quantity + amount)
            .where(Inventory.id == entry.id)
            .execute())
        return Inventory.get_by_id(entry.id).quantity

def remove_item(player_id: int, item_id: str, amount: int = 1) -> tuple[bool, int]:
    
    """移除玩家物品，數量不足時不做任何事並回傳 False
    """
    if amount <= 0:
        raise ValueError("扣除物品的數量必須大於 0")

    # TODO: 與 give_item 有共用片段, 之後將這段檢查取出
    item = data.item.get(item_id)
    if item is None:
        logger.debug(f"錯誤，物品不存在或名稱錯誤: {item_id}")
        return
    if amount <= 0:
        logger.debug(f"錯誤，數量必須為正整數: {amount}")
        return
    
    with database.atomic():
        entry = Inventory.get_or_none(Inventory.player == player_id, Inventory.item_id == item_id)

        if entry is None or entry.quantity < amount:
            return False, entry.quantity if entry else 0

        if entry.quantity == amount:
            entry.delete_instance()
            return True, 0

        (Inventory
            .update(quantity=Inventory.quantity - amount)
            .where(Inventory.id == entry.id)
            .execute())
        return True, Inventory.get_by_id(entry.id).quantity

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