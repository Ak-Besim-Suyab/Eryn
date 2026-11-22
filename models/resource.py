"""該模組為資源欄位, 這個欄位用於存取所有單位資源 (木材, 石材, 食物等等)
"""

from peewee import *  # pyright: ignore[reportWildcardImportFromLibrary]
from cores.database import BaseModel
from .player import Player

class Resource(BaseModel):

    player = ForeignKeyField(Player, backref = 'resources', unique = True, on_delete = 'CASCADE')

    food = IntegerField(default = 0)
    wood = IntegerField(default = 0)
    stone = IntegerField(default = 0)
    iron = IntegerField(default = 0)