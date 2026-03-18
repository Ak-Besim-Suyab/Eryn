from peewee import *
from database.generic import db

from context import Context

class Player(Model):
    # discord fields.
    id = IntegerField(primary_key=True)
    display_name = TextField(default="無名的旅人")

    # game-related fields.
    level = IntegerField(default=1)
    experience = IntegerField(default=0)
    currency = IntegerField(default=0)
    location = TextField(default="Unknown Location")
    
    # others.
    card = TextField(null=True)
    use_pet = IntegerField(default=0)

    timestamp_daily_reward = FloatField(null=True)
    timestamp_voice = FloatField(null=True)

    class Meta:
        database = db


    @classmethod
    def get_or_create_player(cls, user_id: int):
        """獲取或創建玩家，並確保玩家統計資料存在"""
        player, _ = cls.get_or_create(id=user_id)

        # 確保玩家統計資料存在
        # 避免循環調用，導入放在方法內部
        from database.player_statistic import PlayerStatistic
        PlayerStatistic.get_or_create(player=player)

        return player
    
    @classmethod
    def add_balance(cls, user_id: int, amount: int):
        with db.atomic():
            # get_or_create returns (instance, created)
            player, _ = cls.get_or_create(id=user_id)
            player.currency += amount
            player.save()

    @classmethod
    def remove_balance(cls, user_id: int, amount: int):
        with db.atomic():
            player, _ = cls.get_or_create(id=user_id)
            player.currency -= amount
            player.save()

    @staticmethod
    def _get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)

    @classmethod
    def add_experience(cls, player_id: int, amount: int):
        with db.atomic():
            player, _ = cls.get_or_create(id=player_id)
            player.experience += amount

            while player.experience >= player._get_required_exp(player.level):
                player.experience -= player._get_required_exp(player.level)
                player.level += 1

            player.save()
    
    @classmethod
    def save_timestamp_voice(self, player_id: int, timestamp: float):
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = timestamp
            player.save()

    @classmethod
    def remove_timestamp_voice(self, player_id: int):
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = None
            player.save()

    @classmethod
    def get_timestamp_voice(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)
        return player.timestamp_voice
    
    @classmethod
    def save_timestamp_daily_reward(self, player_id: int, timestamp: float):
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_daily_reward = timestamp
            player.save()
    
    @classmethod
    def remove_timestamp_daily_reward(self, player_id: int):
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_daily_reward = None
            player.save()

    @classmethod
    def get_timestamp_daily_reward(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)
        return player.timestamp_daily_reward
    
    @classmethod
    def get_stat(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)

        # 確保玩家統計資料存在，避免在沒有 PlayerStatistic 出現時拋出例外。
        from database.player_statistic import PlayerStatistic
        stat, _ = PlayerStatistic.get_or_create(player=player)

        return stat

def init_player_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Player], safe=True)