from peewee import *
from database.generic import db
from database.player import Player


class Inventory(Model):
    """玩家背包系統 - 儲存物品數量"""
    player = ForeignKeyField(Player, backref='inventory', on_delete='CASCADE')
    item_key = TextField()  # 物品唯一標識符，例如 "salmon", "bass"
    quantity = IntegerField(default=0)

    class Meta:
        database = db
        indexes = (
            (('player', 'item_key'), True),  # 複合唯一鍵：每個玩家每種物品只有一筆記錄
        )
    
    @classmethod
    def add_item(cls, player_id: int, item_key: str, quantity: int = 1) -> int:
        """
        增加物品數量
        
        參數：
            player_id: 玩家 ID
            item_key: 物品鍵值（如 "salmon"）
            quantity: 增加的數量
        
        返回：更新後的總數量
        """
        with db.atomic():
            inventory, created = cls.get_or_create(
                player_id=player_id,
                item_key=item_key,
                defaults={'quantity': 0}
            )
            inventory.quantity += quantity
            inventory.save()
            return inventory.quantity
    
    @classmethod
    def remove_item(cls, player_id: int, item_key: str, quantity: int = 1) -> dict:
        """
        扣除物品數量
        
        參數：
            player_id: 玩家 ID
            item_key: 物品鍵值
            quantity: 扣除的數量
        
        返回：dict，包含：
            {
                'success': True/False,
                'remaining': 剩餘數量,
                'message': 訊息
            }
        """
        with db.atomic():
            try:
                inventory = cls.get(
                    cls.player_id == player_id,
                    cls.item_key == item_key
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
    def get_quantity(cls, player_id: int, item_key: str) -> int:
        """
        查詢物品數量
        
        返回：數量（未持有則返回 0）
        """
        try:
            inventory = cls.get(
                cls.player_id == player_id,
                cls.item_key == item_key
            )
            return inventory.quantity
        except cls.DoesNotExist:
            return 0
    
    @classmethod
    def get_all_items(cls, player_id: int) -> list:
        """
        取得玩家所有物品
        
        返回：Inventory 對象列表（只包含數量 > 0 的）
        """
        return list(cls.select().where(
            (cls.player_id == player_id) & (cls.quantity > 0)
        ))


def init_inventory_database():
    """初始化背包系統數據庫表"""
    with db:
        db.create_tables([Inventory])
