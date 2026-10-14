from peewee import *
from database import BaseModel

from . import Player

"""該模組為道具欄位，與裝備欄位區分，目前僅記錄名稱與數量"""

class Inventory(BaseModel):

    player = ForeignKeyField(Player, backref='houses', on_delete='CASCADE')

    item_id = TextField()
    quantity = IntegerField(default = 0)