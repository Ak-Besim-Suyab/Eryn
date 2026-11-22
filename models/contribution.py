from peewee import *  # pyright: ignore[reportWildcardImportFromLibrary]
from cores.database import BaseModel

from .building import Building
from .player import Player

class Contribution(BaseModel):
    building = ForeignKeyField(Building, backref='contributions', on_delete='CASCADE')  # pyright: ignore[reportUnannotatedClassAttribute]
    player = ForeignKeyField(Player, backref='contributions', on_delete='CASCADE')

    food = IntegerField(default=0)
    wood = IntegerField(default=0)
    stone = IntegerField(default=0)
    iron = IntegerField(default=0)

    class Meta:
        indexes = (
            (('building', 'player'), True),
        )