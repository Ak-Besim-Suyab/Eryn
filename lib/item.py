import discord
import data

from cores.logger import logger
from cores.database import database

from models.player import Player
from models.inventory import Inventory

from data.schema import Item

def is_valid(item_id: str, amount: int) -> bool:
    item = data.item.get(item_id)
    if item is None:
        logger.warning(f"警告，出現未定義或名稱錯誤的物品: {item_id}")
        return False
    if amount <= 0:
        logger.warning(f"警告，數量必須為正整數: {amount}")
        return False
    
    return True

def give(interaction: discord.Interaction | discord.abc.User, item_id: str, amount: int = 1) -> int:
    """ Give player specific item, return quantity after operation.
    """ 
    if not is_valid(item_id, amount):
        return
    
    # 取得使用者物件
    user = interaction.user if isinstance(interaction, discord.Interaction) else interaction

    # 確保玩家存在
    Player.get_or_create(id=user.id)
    with database.atomic():
        entry, _ = Inventory.get_or_create(player = user.id, item_id = item_id, defaults = {"quantity": 0})
        
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
    """ 格式化物品摘要並返回顯示字串，包括圖示和名稱。
    """
    item = data.item.get(item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {item_id}")
        return f"- ❓{item_id} - {quantity}"
    
    return f"- {item.icon}{item.name} - {quantity} "

def detail_line(item_id: str, quantity: int) -> str:
    """ 格式化物品詳細資訊並返回顯示字串，包括所有資訊。
    """
    pass