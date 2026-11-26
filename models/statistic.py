"""
此模塊定義與管理玩家的統計數據
"""
from peewee import * 
from cores.database import BaseModel
from .player import Player

class Statistic(BaseModel):

    player = ForeignKeyField(Player, backref="statistics", unique=True, on_delete="CASCADE")

    total_daily   = IntegerField(default=0)
    total_voice   = IntegerField(default=0)
    total_message = IntegerField(default=0)


class FishStatistic(BaseModel):

    player = ForeignKeyField(Player, backref="fish_statistics", on_delete="CASCADE")

    name  = TextField()
    count = IntegerField(default=0)
    size  = FloatField(default=0.0)

    class Meta:
        indexes = (
            (("player", "name"), True),
        )