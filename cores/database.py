from peewee import SqliteDatabase, Model
from config import DATABASE_PATH

db = SqliteDatabase(DATABASE_PATH)

class BaseModel(Model):
    class Meta:
        database = db