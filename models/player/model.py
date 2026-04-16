from peewee import *
from config import db

from datetime import datetime

class Player(Model):
    # discord fields.
    id = IntegerField(primary_key=True)
    display_name = TextField(default="無名的旅人")

    # game-related fields.
    level = IntegerField(default=1)
    experience = IntegerField(default=0)
    currency = IntegerField(default=0)
    region = TextField(default="falun")
    luck = FloatField(default=1.0)
    karma = IntegerField(default=100)
    
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
        from models.statistic import Statistic
        Statistic.get_or_create(player=player)

        return player
    
    @classmethod
    def add_balance(cls, user_id: int, amount: int):
        with db.atomic():
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

# timestamp_voice methods --------------------------------------------------

    @classmethod
    def save_timestamp_voice(self, player_id: int):
        """
        保存玩家進入語音的時間戳記
        這個方法會保存實作時的時間戳記
        """
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = datetime.now().timestamp()
            player.save()

    @classmethod
    def remove_timestamp_voice(self, player_id: int):
        """
        移除玩家的語音時間戳記
        這個方法會直接將時間戳記設為 None
        """
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = None
            player.save()

    @classmethod
    def get_timestamp_voice(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)
        return player.timestamp_voice

# --------------------------------------------------------------------------
# timestamp_daily_reward methods -------------------------------------------

    @classmethod
    def save_timestamp_daily_reward(self, player_id: int):
        """
        保存玩家取得每日獎勵的時間戳記
        這個方法會保存實作時的時間戳記
        """
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_daily_reward = datetime.now().timestamp()
            player.save()
    
    @classmethod
    def remove_timestamp_daily_reward(self, player_id: int):
        """
        移除玩家的每日獎勵時間戳記
        這個方法會直接將時間戳記設為 None
        """
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_daily_reward = None
            player.save()

    @classmethod
    def get_timestamp_daily_reward(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)
        return player.timestamp_daily_reward

# --------------------------------------------------------------------------

    @classmethod
    def get_stat(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)

        # 確保玩家統計資料存在，避免在沒有 PlayerStatistic 出現時拋出例外。
        from models.statistic import Statistic
        stat, _ = Statistic.get_or_create(player=player)

        return stat

# --------------------------------------------------------------------------

    @classmethod
    def get_region(self, player_id: int) -> str:
        """
        獲取玩家所在地區，這裡返回的是 Region ID
        """
        player, _ = self.get_or_create(id=player_id)
        return player.region
    
    @classmethod
    def set_region(self, player_id: int, region: str):
        with db.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.region = region
            player.save()

def init_player_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Player], safe=True)