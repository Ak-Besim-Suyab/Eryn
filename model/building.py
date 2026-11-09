from peewee import *
from cores.database import BaseModel

class Building(BaseModel):
    id = TextField(primary_key=True, unique=True)
    
    level = IntegerField(default=1)