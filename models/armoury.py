from peewee import *
from database import BaseModel

from . import Player

"""該模組為裝備欄位，與道具欄位區分"""

class Inventory(BaseModel):

    player = ForeignKeyField(Player, backref='houses', on_delete='CASCADE')

    item_id = TextField()