from peewee import *
from database.generic import db

class Player(Model):
    id = IntegerField(primary_key=True)  # Discord 用戶 ID
    display_name = TextField(default="Unknown")
    currency_yab = IntegerField(default=0)  # 貨幣
    card = TextField(null=True)
    use_pet = IntegerField(default=0)

    class Meta:
        database = db

    @classmethod
    def get_or_create_player(cls, user_id: int):
        """獲取或創建玩家"""
        player, created = cls.get_or_create(id=user_id)
        return player

    @classmethod
    def increase_currency(cls, user_id: int, amount: int = 0):
        """增加貨幣"""
        with db.atomic():
            player = cls.get_or_create_player(user_id)
            player.currency_yab += amount
            player.save()

    @classmethod
    def decrease_currency(cls, user_id: int, amount: int = 0):
        """減少貨幣"""
        with db.atomic():
            player = cls.get_or_create_player(user_id)
            player.currency_yab -= amount
            player.save()

    @classmethod
    def increase_use_pet(cls, user_id: int, amount: int = 0):
        """增加撫摸次數"""
        with db.atomic():
            player = cls.get_or_create_player(user_id)
            player.use_pet += amount
            player.save()
        return player.use_pet

def init_player_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Player], safe=True)