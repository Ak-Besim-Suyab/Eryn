from peewee import *
from cores.database import BaseModel
from models import Player

class ItemInstance(BaseModel):
    """
    這個模組用於紀錄玩家所有可裝備的物品槽位，泛指裝備、技能等可穿戴或拆卸的系統
    .. slot::
        裝備槽位，與`owner`組成唯一鍵，槽位名稱由`unknown`控制
    """
    player = ForeignKeyField(Player, backref = 'equipments', on_delete = 'CASCADE')
    item_id = TextField()
    slot = TextField(null = True)

    class Meta:
        indexes = (
            (('player', 'slot'), True),
        )