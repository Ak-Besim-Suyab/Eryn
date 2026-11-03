from peewee import *
from cores.database import BaseModel
from models.item_instance import ItemInstance

class ItemAffix(BaseModel):
    item = ForeignKeyField(ItemInstance, backref='affixes', on_delete='CASCADE')
    type = TextField()
    modifier = TextField()
    value = IntegerField()