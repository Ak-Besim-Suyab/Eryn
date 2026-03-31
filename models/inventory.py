from peewee import *
from models.generic import db
from models.player import Player

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
    def add_item(cls, player_id: int, item_id: str, quantity: int = 1) -> int:
        with db.atomic():
            inventory, _ = cls.get_or_create(player_id=player_id, item_id=item_id)
            inventory.quantity += quantity
            inventory.save()

        logger.debug(f"[InventorySystem] 添加 {quantity} 個 {item_id} 到 {player_id} 的背包")

    @classmethod
    def remove_item(cls, player_id: int, item_id: str, quantity: int = 1) -> dict:
        """移除物品數量，返回操作結果字典"""
        with db.atomic():
            try:
                inventory = cls.get(cls.player_id == player_id, cls.item_id == item_id)
                
                if inventory.quantity < quantity:
                    return {
                        'success': False,
                        'remaining': inventory.quantity,
                        'message': f'數量不足（擁有 {inventory.quantity}，需要 {quantity}）'
                    }
                
                inventory.quantity -= quantity
                inventory.save()
                
                return {
                    'success': True,
                    'remaining': inventory.quantity,
                    'message': '成功扣除'
                }
            
            except cls.DoesNotExist:
                return {
                    'success': False,
                    'remaining': 0,
                    'message': '未持有此物品'
                }
            
    @classmethod
    def has_item(cls, player_id: int, item_id: str, required_quantity: int = 1) -> bool:
        """檢查玩家是否擁有足夠的物品數量"""
        return cls.get_quantity(player_id, item_id) >= required_quantity

    @classmethod
    def get_quantity(cls, player_id: int, item_id: str) -> int:
        """查詢物品數量並返回數量，未持有則返回 0 """
        try:
            inventory = cls.get(
                cls.player_id == player_id,
                cls.item_id == item_id
            )
            return inventory.quantity
        except cls.DoesNotExist:
            return 0
    
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
