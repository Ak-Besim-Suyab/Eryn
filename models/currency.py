from peewee import *
from cores.database import BaseModel
from .player import Player

class Currency(BaseModel):

    player = ForeignKeyField(Player, backref = 'currencies', unique = True, on_delete = 'CASCADE')

    vin = IntegerField(default = 0)