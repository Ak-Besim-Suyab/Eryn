from peewee import *
from models.generic import db
from models.player import Player

class PlayerStatistic(Model):
    player = ForeignKeyField(Player, backref='stats', unique=True, on_delete='CASCADE')
    
    total_daily_claims = IntegerField(default=0)

    class Meta:
        database = db

def init_player_statistic_database():
    with db:
        db.create_tables([PlayerStatistic], safe=True)