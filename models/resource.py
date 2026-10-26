"""該模組為資源欄位, 這個欄位用於存取所有單位資源 (木材, 石材, 食物等等)
"""

from peewee import *
from cores.database import BaseModel
from models import Player

class Resource(BaseModel):

    player = ForeignKeyField(Player, backref = 'resource', on_delete = 'CASCADE')

    wood = IntegerField(default = 0)
    stone = IntegerField(default = 0)
    food = IntegerField(default = 0)

    class Meta:
        indexes = ((('player', 'item_id'), True),)