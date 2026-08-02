from peewee import *

from database import BaseModel, db

from . import Player

class House(BaseModel):

    player_id = ForeignKeyField(Player, backref='houses', on_delete='CASCADE')
    channel_id = IntegerField(unique=True)
