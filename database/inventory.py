from peewee import *
from database.generic import db
from database.player import Player


class Inventory(Model):
    player = ForeignKeyField(Player, backref = 'inventory', on_delete = 'CASCADE')
    item_id = TextField()  # 物品唯一標識符，例如 "salmon", "bass"
    quantity = IntegerField(default = 0)

    class Meta:
        database = db
        indexes = (
            (('player', 'item_id'), True),  # 複合唯一鍵，確保每個玩家每種物品只有一筆記錄
        )
    
    @classmethod
    def add_item(cls, player_id: int, item_id: str, quantity: int = 1) -> int:
        """增加物品數量"""
        with db.atomic():
            inventory, created = cls.get_or_create(
                player_id=player_id,
                item_id=item_id,
                defaults={'quantity': 0}
            )
            inventory.quantity += quantity
            inventory.save()

    @classmethod
    def remove_item(cls, player_id: int, item_id: str, quantity: int = 1) -> dict:
        """移除物品數量，返回操作結果字典"""
        with db.atomic():
            try:
                inventory = cls.get(
                    cls.player_id == player_id,
                    cls.item_id == item_id
                )
                
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
    def get_all_items(cls, player_id: int) -> list:
        """取得玩家所有物品，返回 list """
        return list(cls.select().where(
            (cls.player_id == player_id) & (cls.quantity > 0)
        ))


def init_inventory_database():
    """初始化背包系統數據庫表"""
    with db:
        db.create_tables([Inventory], safe=True)
