from peewee import *
from config import db
from models.player.model import Player

from cores.logger import logger

class Inventory(Model):
    player_id = ForeignKeyField(Player, backref = 'inventory', on_delete = 'CASCADE')
    item_id = TextField()
    quantity = IntegerField(default = 0)

    class Meta:
        database = db
        indexes = (
            (('player_id', 'item_id'), True),  # 複合唯一鍵，確保每個玩家每種物品只有一筆記錄
        )
    
    @classmethod
    def add_item(cls, player_id: int, item_id: str, quantity: int = 1):
        with db.atomic():
            item, _ = cls.get_or_create(player_id=player_id, item_id=item_id)
            item.quantity += quantity
            item.save()
            logger.debug(f"成功添加 {quantity} 個 {item_id} 到 {player_id} 的背包")

    @classmethod
    def remove_item(cls, player_id: int, item_id: str, quantity: int = 1) -> bool:
        """移除物品數量，返回操作結果字典"""
        with db.atomic():
            # 如果要移除的物品數量錯誤，返回失敗
            if quantity <= 0: 
                logger.warning(f"要移除的物品數量錯誤： {quantity}")
                return False

            item = cls.get_or_none(player_id=player_id, item_id=item_id)

            if item is None or item.quantity < quantity: 
                return False

            item.quantity -= quantity
            item.save()
            logger.debug(f"成功移除 {quantity} 個 {item_id} 從 {player_id} 的背包")
            return True

    @classmethod
    def get_item(cls, player_id: int, item_id: str) -> Inventory | None:
        try:
            item = cls.get(
                cls.player_id == player_id,
                cls.item_id == item_id
            )
            return item
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_inventory(cls, player_id: int) -> dict:
        """獲取玩家的背包內容"""
        items = cls.select().where(cls.player_id == player_id, cls.quantity > 0)

        inventory = {}
        for item in items:
            inventory[item.item_id] = item.quantity

        return inventory

def init_inventory_database():
    """初始化背包系統數據庫表"""
    with db:
        db.create_tables([Inventory], safe=True)
