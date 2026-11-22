from peewee import *  # pyright: ignore[reportWildcardImportFromLibrary]
from cores.database import BaseModel

class Building(BaseModel):
    id = TextField(primary_key=True)
    
    level = IntegerField(default=1)
    experience = FloatField(default=0.0)