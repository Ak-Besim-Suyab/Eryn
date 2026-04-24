from peewee import *
from config import db
from game.model import Player

class Statistic(Model):
    """
    這個模塊用於定義與管理玩家的統計數據
    """
    player = ForeignKeyField(Player, backref='stats', unique=True, on_delete='CASCADE')
    
    total_daily_claims = IntegerField(default=0)
    total_voice_time = IntegerField(default=0)

    class Meta:
        database = db

def init_statistic_database():
    with db:
        db.create_tables([Statistic], safe=True)