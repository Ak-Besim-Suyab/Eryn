from peewee import *
from database.generic import db

class Player(Model):
    id = IntegerField(primary_key = True)
    display_name = TextField(default = "default")

    card = TextField(null=True)

    currency_yab = IntegerField(default = 0)

    use_pet = IntegerField(default = 0)

    class Meta:
        database = db

    @classmethod
    def get_or_create_player(cls, id: int):
        player, created = cls.get_or_create(id=id)
        return player

    @classmethod
    def increase_currency(cls, id: int, amount:int = 0):
        with db.atomic():
            player = cls.get_or_create_player(id)
            player.currency_yab += amount
            player.save()

    @classmethod
    def decrease_currency(cls, id: int, amount:int = 0):
        with db.atomic():
            player = cls.get_or_create_player(id)
            player.currency_yab -= amount
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