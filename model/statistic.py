from peewee import *
from cores.database import BaseModel, database

"""
這個模塊用於定義與管理玩家的統計數據
"""

class Statistic(BaseModel):

    id = IntegerField(primary_key=True)
    display_name = TextField(default="無名的旅人")

    total_daily = IntegerField(default=0)
    total_voice = IntegerField(default=0)
    total_message = IntegerField(default=0)

    @classmethod
    def get_or_create_stat(cls, user_id: int) -> Statistic:
        stat, _ = cls.get_or_create(id=user_id)
        return stat