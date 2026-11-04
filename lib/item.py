from data import ITEMS

from cores.logger import logger
from cores.database import database

from models.player import Player
from models.inventory import Inventory
from models.item_instance import ItemInstance

def is_valid(item_id: str, amount: int) -> bool:
    """ 驗證執行邏輯的物品與數量是否合法，全數通過後回傳資料物件
    """
    item = ITEMS.get(item_id)
    if item is None:
        logger.warning(f"警告，出現未定義或名稱錯誤的物品: {item_id}")
        return False
    if amount <= 0:
        logger.warning(f"警告，數量必須為正整數: {amount}")
        return False
    
    return item, True

def give(player_id: int, item_id: str, amount: int = 1) -> int:
    """ 給予玩家物品，返回給予後的持有數量
    """ 
    if not is_valid(item_id, amount):
        return
    
    # 確保玩家存在
    Player.get_or_create(id=player_id)

    item = ITEMS.get(item_id)

    if item is None:
        return

    if item.is_equippable():
        with database.atomic():
            instance = ItemInstance.create(player=player_id, item_id=item_id)

            #NOTE: 這裡未來可能需要實作將獲得物品時得到的隨機詞綴存入 ItemAffix 資料表

        return instance

    with database.atomic():
        entry, _ = Inventory.get_or_create(player=player_id, item_id=item_id, defaults={"quantity": 0})
        
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

        logger.debug(f"成功移除 {player_id} 的物品: {item_id}")
        
        return True, Inventory.get_by_id(entry.id).quantity

# function for formatting item display.
def summary_line(item_id: str, quantity: int) -> str:
    """ 
    搜尋物品表並返回訊息用的文字字串，僅包含數量、圖示和顯示名稱。
    """
    item = ITEMS.get(item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {item_id}")
        return f"{quantity} ❓{item_id}"
    
    return f"{quantity} {item.icon}{item.name}"

def description(item_id: str, quantity: int, type: str = "summary") -> str:
    """
    return descriptions of item.
    """
    item = ITEMS.get(item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {item_id}")
        return f"{quantity} ❓{item_id}"

    match type:
        case "summary":
            return f"{quantity} {item.icon}{item.name}"
        case "detail":
            return f"{quantity} {item.icon}{item.name}\n{item.description}"