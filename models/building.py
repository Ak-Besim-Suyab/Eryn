from peewee import *
from cores.database import BaseModel

class Building(BaseModel):
    id = IntegerField(primary_key=True, unique=True)
    
    level = IntegerField(default=1)
    experience = IntegerField(default=0)