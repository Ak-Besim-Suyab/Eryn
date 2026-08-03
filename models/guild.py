from peewee import *
from database import BaseModel, db

class Guild(BaseModel):
    id = IntegerField(primary_key=True)
    announcement_channel = IntegerField(null=True)
    
    @classmethod
    def set_announcement_channel(cls, guild_id: int, channel_id: int) -> None:
        with db.atomic():
            guild, _ = cls.get_or_create(id=guild_id)
            guild.announcement_channel = channel_id
            guild.save()
    
    @classmethod
    def get_announcement_channel(cls, guild_id: int) -> int:
        guild, _ = cls.get_or_create(id=guild_id)
        return guild.announcement_channel

def init_guild_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Guild], safe=True)