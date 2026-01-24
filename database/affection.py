from peewee import *
from database.player import Player
from database.dummy import Dummy
from database.generic import db 

class Affection(Model):
    # affection in Player.affections:
    # affection.level = 0 - 100
    player = ForeignKeyField(Player, backref='affections')
    dummy = ForeignKeyField(Dummy, backref='affections')

    level = IntegerField(default=0)

    class Meta:
        database = db
        indexes = (
            (('player', 'dummy'), True),
        )

    @classmethod
    def increase_affection(cls, player_id: int, dummy_id: int, amount:int = 1):
        with db.atomic():
            affection, created = cls.get_or_create(
                player=player_id, 
                dummy=dummy_id
            )
            affection.level += amount
            affection.save()
            return affection.level

def init_affection_database():
    with db:
        db.create_tables([Affection], safe=True)