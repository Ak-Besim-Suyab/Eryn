from peewee import *
from cores.database import BaseModel

from models import Building
from models import Player

class Contribution(BaseModel):
    building = ForeignKeyField(Building, backref='contributions', on_delete='CASCADE')
    player = ForeignKeyField(Player, backref='contributions', on_delete='CASCADE')

    wood = IntegerField(default=0)
    stone = IntegerField(default=0)
    food = IntegerField(default=0)

    class Meta:
        indexes = (
            (('building', 'player'), True),
        )