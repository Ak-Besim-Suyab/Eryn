from peewee import *
from cores.database import BaseModel

from models import Player

"""該模組為裝備欄位，與道具欄位區分
"""

class Armoury(BaseModel):

    player = ForeignKeyField(Player, backref='armoury', on_delete='CASCADE')

    item_id = TextField()