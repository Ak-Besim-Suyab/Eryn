from peewee import *
from database.generic import db

class Dummy(Model):
    id = IntegerField(primary_key = True)
    display_name = TextField(default = "dummy")

    pets = IntegerField(default = 0)

    class Meta:
        database = db

    @classmethod
    def fetch(cls, id: int):
        dummy, created_dummy = cls.get_or_create(id = id)
        return dummy

    @classmethod
    def increase_pets(cls, dummy_id: int, amount:int = 1):
        with db.atomic():
            dummy = cls.fetch(dummy_id)
            dummy.pets += amount
            dummy.save()
        return dummy.pets

def init_dummy_database():
    with db:
        db.create_tables([Dummy])