"""
此模塊定義與管理玩家的統計數據
"""
from peewee import * 
from cores.database import BaseModel
from .player import Player

class Statistic(BaseModel):

    player = ForeignKeyField(Player, backref="statistics", unique=True, on_delete="CASCADE")

    total_daily = IntegerField(default=0)
    total_voice = IntegerField(default=0)
    total_message = IntegerField(default=0)

    @classmethod
    def get_or_create_stat(cls, player_id: int) -> "Statistic":
        stat, _ = cls.get_or_create(player_id=player_id)
        return stat