"""該模組為材料欄位, 這個欄位用於存取所有單位材料 (木材, 石材, 食物等等)
"""

from peewee import *
from cores.database import BaseModel
from .player import Player

class Material(BaseModel):

    player = ForeignKeyField(Player, backref = 'materials', unique = True, on_delete = 'CASCADE')

    food = IntegerField(default = 0)
    wood = IntegerField(default = 0)
    stone = IntegerField(default = 0)
    iron = IntegerField(default = 0)
