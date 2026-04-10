"""
考慮到未來設計的狀態，比如疲勞、飢餓，某些狀態會基於數值更新，某些則以狀態本身的層數更新
基於數值更新的狀態，邏輯會丟在更新數值的方法內處理，基於狀態更新的狀態則在這裡處理

比如倒楣蛋升級為逆轉命運 (說是升級，也可以說是轉換，但基本上是共用邏輯，而非語言上的線性或變更處理)
現在的設計思路為：為 status data 新增一個屬性，用來判定滿層數後會更換或新增、移除什麼狀態
"""
from peewee import *
from config import db
from models.player import Player
from models.type import StatusType
from cores.logger import logger

from .data.status import status_manager

class Status(Model):
    """
    這個模塊用於定義與管理玩家狀態，這裡只負責保存玩家狀態，關於個別狀態的管理、邏輯、行為則由 StatusManager 負責
    """
    player_id = ForeignKeyField(Player, backref = 'statuses', on_delete = 'CASCADE')
    status_id = TextField()
    stack = IntegerField(default = 0)

    class Meta:
        database = db
        indexes = (
            (('player_id', 'status_id'), True),  # 複合唯一鍵，確保每個玩家每種物品只有一筆記錄
        )

    @classmethod
    def add(cls, player_id: int, status_id: StatusType, quantity: int = 1):
        with db.atomic():
            status, _ = cls.get_or_create(player_id=player_id, status_id=status_id)
            status_data = status_manager.get(status_id)

            if status_data is None:
                logger.warning(f"找不到狀態 {status_id}")
                return

            if status.stack + quantity > status_data.stack.max:
                status.stack = status_data.stack.max
            else:
                status.stack += quantity
            status.save()

            logger.debug(f"成功為 {player_id} 添加狀態 {status_id}")
    
    @classmethod
    def remove(cls, player_id: int, status_id: str, quantity: int = 1) -> bool:
        with db.atomic():
            # 數量為負數的話回報警告，由於數量錯誤可以判定為不移除，因此只回傳 False
            if quantity <= 0:
                logger.warning(f"要移除的狀態數量錯誤, 移除狀態的數量不能為負數, 本次移除的數量為 {quantity}")
                return False
            
            status = cls.get_or_none(player_id=player_id, status_id=status_id)

            # 如果狀態為 None 代表沒有可移除的狀態
            if status is None:
                return False
            
            status.stack -= quantity
            if status.stack <= 0:
                status.delete_instance()
                logger.debug(f"成功移除 {player_id} 的狀態 {status_id}")
                return True
            else:
                status.save()
                logger.debug(f"成功為 {player_id} 移除 {quantity} 層 {status_id} 狀態")
                return True

def init_status_database():
    with db:
        db.create_tables([Status], safe=True)