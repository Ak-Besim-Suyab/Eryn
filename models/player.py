from peewee import *
from cores.database import BaseModel

class Player(BaseModel):

    id           = IntegerField(primary_key=True)
    display_name = TextField(default="無名的旅人")
    level        = IntegerField(default=1)
    experience   = FloatField(default=0.0)

    race   = TextField(default="yemir")
    region = TextField(default="port_norse")

    turn = IntegerField(default=0)
    
    card = TextField(null=True)
    use_pet = IntegerField(default=0)

    timestamp_daily = FloatField(null=True)
    timestamp_voice = FloatField(null=True)

class Attribute(BaseModel):
    player = ForeignKeyField(Player, backref = "attributes", on_delete = "CASCADE")
    
    # 基礎屬性
    strength     = IntegerField(default=0)   # 力量
    constitution = IntegerField(default=0)   # 體質
    dexterity    = IntegerField(default=0)   # 敏捷
    perception   = IntegerField(default=0)   # 感知
    intelligence = IntegerField(default=0)   # 智力
    charisma     = IntegerField(default=0)   # 魅力

    # 其他屬性
    luck         = IntegerField(default=0)   # 幸運
    sanity       = IntegerField(default=100) # 理智
    karma        = IntegerField(default=20)  # 善惡