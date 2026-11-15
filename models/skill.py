from peewee import *
from cores.database import BaseModel
from models import Player

class Skill(BaseModel):
    player = ForeignKeyField(Player, backref = 'skill', on_delete = 'CASCADE')

    name = TextField()
    level = IntegerField(default = 1)
    experience = IntegerField(default = 0)

    class Meta:
        indexes = (
            (('player', 'name'), True),
        )