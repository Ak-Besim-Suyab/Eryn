"""該模組為道具欄位，與裝備欄位區分，目前僅記錄名稱與數量
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