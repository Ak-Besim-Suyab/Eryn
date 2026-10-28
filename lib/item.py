import data

from cores.logger import logger
from cores.database import database

from models.player import Player
from models.inventory import Inventory

def is_valid(item_id: str, amount: int) -> bool:
    item = data.item.get(item_id)
    if item is None:
        logger.warning(f"警告，出現未定義或名稱錯誤的物品: {item_id}")
        return False
    if amount <= 0:
        logger.warning(f"警告，數量必須為正整數: {amount}")
        return False
    
    return True

def give(player_id: int, item_id: str, amount: int = 1) -> int:
    """給予玩家物品，回傳運算後的持有數量
    """
    if not is_valid(item_id, amount):
        return

    # 確保玩家存在
    Player.get_or_create(id=player_id)
    with database.atomic():
        entry, _ = Inventory.get_or_create(player = player_id, item_id = item_id, defaults = {"quantity": 0})
        
        (Inventory
            .update(quantity = Inventory.quantity + amount)
            .where(Inventory.id == entry.id)
            .execute())
        return Inventory.get_by_id(entry.id).quantity

def remove(player_id: int, item_id: str, amount: int = 1) -> tuple[bool, int]:
    """移除玩家物品，回傳是否移除成功以及運算後的持有數量
    """
    if not is_valid(item_id, amount):
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

def open(player_id: int, item_id: str, amount: int = 1):
    with database.atomic():
        success, remaining = remove(player_id, item_id, amount)
        if not success:
            return

        item = data.item.get(item_id)
        rewards = item.roll()

        for (reward_type, reward_id), amount in rewards.items():
            give(player_id, reward_id, amount)

def consume(player_id: int, item_id: str, amount: int = 1):
    with database.atomic():
        success, remaining = remove(player_id, item_id, amount)
        if not success:
            return

        # ...