from peewee import *
from cores.database import BaseModel, database

from datetime import datetime

class Player(BaseModel):

    id = IntegerField(primary_key=True, unique=True)

    display_name = TextField(default="無名的旅人")
    level = IntegerField(default=1)
    experience = IntegerField(default=0)

    currency = IntegerField(default=0)
    region = TextField(default="falun")

    san = FloatField(default=100.0)
    luck = FloatField(default=1.0)
    karma = FloatField(default=100.0)
    
    card = TextField(null=True)
    use_pet = IntegerField(default=0)

    timestamp_daily = FloatField(null=True)
    timestamp_voice = FloatField(null=True)

    @staticmethod
    def get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)

    @classmethod
    def add_experience(cls, player_id: int, amount: int):
        with database.atomic():
            player: Player
            player, _ = cls.get_or_create(id=player_id)
            player.experience += amount

            while player.experience >= player.get_required_exp(player.level):
                player.experience -= player.get_required_exp(player.level)
                player.level += 1

            player.save()

# timestamp_voice methods --------------------------------------------------

    @classmethod
    def save_timestamp_voice(self, player_id: int):
        """
        保存玩家進入語音的時間戳記
        這個方法會保存實作時的時間戳記
        """
        with database.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = datetime.now().timestamp()
            player.save()

    @classmethod
    def remove_timestamp_voice(self, player_id: int):
        """
        移除玩家的語音時間戳記
        這個方法會直接將時間戳記設為 None
        """
        with database.atomic():
            player, _ = self.get_or_create(id=player_id)
            player.timestamp_voice = None
            player.save()

    @classmethod
    def get_timestamp_voice(self, player_id: int):
        player, _ = self.get_or_create(id=player_id)
        return player.timestamp_voice