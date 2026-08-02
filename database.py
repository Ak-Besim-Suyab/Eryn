import os
from peewee import SqliteDatabase, Model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "generic.db")

db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db