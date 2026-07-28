from peewee import *
from config import db

class Statistic(Model):
    """
    這個模塊用於定義與管理玩家的統計數據。
    id 代表玩家 ID，這樣可以獨立保存統計資料而不依賴外鍵。
    """
    id = IntegerField(primary_key=True)
    display_name = TextField(default="無名的旅人")

    total_daily_claims = IntegerField(default=0)
    total_voice_time = IntegerField(default=0)
    total_message_send = IntegerField(default=0)

    class Meta:
        database = db

    @classmethod
    def get_or_create_stat(cls, **kwargs):
        return cls.get_or_create(**kwargs)


def init_statistic_database():
    with db:
        db.create_tables([Statistic], safe=True)