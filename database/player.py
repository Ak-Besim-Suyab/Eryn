from peewee import *
from database.generic import db

class Player(Model):
    uid = IntegerField(primary_key = True)
    name = TextField(default = "Unknown")
    currency = IntegerField(default = 0)

    card = TextField(null=True)

    use_pet = IntegerField(default = 0)

    class Meta:
        database = db

    @classmethod
    def get_or_create_player(cls, uid: int):
        player, created = cls.get_or_create(uid=uid)
        return player

    @classmethod
    def increase_currency(cls, id: int, amount:int = 0):
        with db.atomic():
            player = cls.get_or_create_player(id)
            player.currency += amount
            player.save()

    @classmethod
    def decrease_currency(cls, id: int, amount:int = 0):
        with db.atomic():
            player = cls.get_or_create_player(id)
            player.currency -= amount
            player.save()

    @classmethod
    def increase_use_pet(cls, id: int, amount:int = 0):
        with db.atomic():
            player = cls.get_or_create_player(id)
            player.use_pet += amount
            player.save()
        return player.use_pet

def init_player_database():
    with db:
        db.create_tables([Player])