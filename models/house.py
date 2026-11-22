"""小屋模塊, 用於紀錄成員的小屋頻道 ID"""

from peewee import *
from cores.database import BaseModel

from .player import Player

class House(BaseModel):

    owner = ForeignKeyField(Player, backref='houses', on_delete='CASCADE')

    id = IntegerField(primary_key=True)