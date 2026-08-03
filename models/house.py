from peewee import *
from database import BaseModel

from . import Player

"""這是社群專用模塊, 用於紀錄成員的小屋頻道 ID"""

class House(BaseModel):

    owner = ForeignKeyField(Player, backref='houses', on_delete='CASCADE')
    id = IntegerField(primary_key=True)