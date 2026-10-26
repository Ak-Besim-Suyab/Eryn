"""該模組為道具欄位, 以道具名稱與數量進行紀錄, 這個欄位無法存取任何道具狀態
"""

from peewee import *
from cores.database import BaseModel
from models import Player

class Inventory(BaseModel):

    player = ForeignKeyField(Player, backref = 'inventory', on_delete = 'CASCADE')

    item_id = TextField()
    quantity = IntegerField(default = 0)

    class Meta:
        indexes = ((('player', 'item_id'), True),)