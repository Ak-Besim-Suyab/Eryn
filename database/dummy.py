from peewee import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "dummy.db")

dummy_database = SqliteDatabase(DB_PATH)

class Dummy(Model):
    id = IntegerField(primary_key = True)
    display_name = TextField(default = "dummy")

    pet_count = IntegerField(default = 0)

    class Meta:
        database = dummy_database

    @classmethod
    def fetch(cls, id: int):
        dummy, created_dummy = cls.get_or_create(id = id)
        return dummy

def init_dummy_database():
    with dummy_database:
        dummy_database.create_tables([Dummy])