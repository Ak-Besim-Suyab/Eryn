from data import ITEMS, SLOTS
from data.schema.item_component import EQUIPMENT

from cores.logger import logger
from cores.database import database

from models.player import Player
from models.inventory import Inventory
from models.item_instance import ItemInstance

def is_valid(item_id: str, amount: int) -> bool:
    """ 
    驗證物品與數量是否合法
    """
    item = ITEMS.get(item_id)
    
    if item is None:
        logger.warning(f"警告，出現未定義或名稱錯誤的物品: {item_id}")
        return False

    if amount <= 0:
        logger.warning(f"警告，數量必須為正整數: {amount}")
        return False
    
    return True

def give(player_id: int, item_id: str, amount: int = 1) -> bool:
    """ 給予玩家物品，返回給予後的持有數量
    """ 
    if not is_valid(item_id, amount):
        return
    
    # 確保玩家存在
    Player.get_or_create(id=player_id)

    item = ITEMS.get(item_id)

    if item is None:
        return False

    if item.has(EQUIPMENT):
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
    
    logger.debug(f"成功給予 {player_id} {amount} {item_id} (item)")
        
    return True

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

        logger.debug(f"成功移除 {player_id} {amount} {item_id} (item)")
        
        return True, Inventory.get_by_id(entry.id).quantity

def fmtstr_short(item_id: str, quantity: int):
    item = ITEMS.get(item_id)
    return f"{item.icon} {item.name} ‧ {quantity}" if is_valid(item_id, quantity) else f"❓ {item_id} ‧ {quantity}"

# function for formatting item display.
def summary_line(item_id: str, quantity: int) -> str:
    """ 
    搜尋物品表並返回訊息用的文字字串，僅包含數量、圖示和顯示名稱。
    """
    item = ITEMS.get(item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {item_id}")
        return f"{quantity} ❓ {item_id}"

    if item.has_tags("equipment"):
        lines = [
            f"**{item.icon} {item.name}**",
            f"-# {item.tooltip}",
        ]
        return "\n".join(lines)
    
    lines = [
        f"**{item.icon} {item.name} ‧ {quantity}**",
        f"> -# {item.tooltip}",
    ]
    
    return "\n".join(lines)

def sort_key(row: Inventory | ItemInstance) -> tuple[float, str]:
    item = ITEMS.get(row.item_id)
    return (item.serial if item else 9999, row.item_id)

def equip_sort_key(row: ItemInstance) -> tuple[int, str]:
    """
    這個函式用於返回物品可裝備欄位的序列號碼, 用於裝備欄位排序
    """
    slot = SLOTS.get(row.slot)
    return (slot.serial if slot else 99, row.item_id)