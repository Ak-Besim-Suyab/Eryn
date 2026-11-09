from peewee import *
from cores.database import BaseModel
from model.item_instance import ItemInstance

class ItemAffix(BaseModel):
    item = ForeignKeyField(ItemInstance, backref='affixes', on_delete='CASCADE')
    scope = TextField()
    stat = TextField()
    operator = TextField()
    value = IntegerField()