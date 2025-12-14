from peewee import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "player.db")

player_database = SqliteDatabase(DB_PATH)

class Player(Model):
    id = IntegerField(primary_key = True)
    display_name = TextField(default = "default")

    card = TextField(null=True)

    currency_yab = IntegerField(default = 0)

    class Meta:
        database = player_database

    @classmethod
    def fetch(cls, id: int):
        player, created_player = cls.get_or_create(id = id)
        return player

    @classmethod
    def increase_currency(cls, id: int, amount:int = 0):
        with player_database.atomic():
            player = cls.fetch(id)
            player.currency_yab += amount
            player.save()

    @classmethod
    def decrease_currency(cls, id: int, amount:int = 0):
        with player_database.atomic():
            player = cls.fetch(id)
            player.currency_yab -= amount
            player.save()

def init_player_database():
    with player_database:
        player_database.create_tables([Player])