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
    def get_or_create_player(cls, user_id: int, display_name: str):
        """獲取或創建玩家，並確保玩家統計資料存在"""
        player, created = cls.get_or_create(id=user_id)

        # 保存名稱，如果玩家已存在但名稱不同，則更新名稱
        if player.display_name != display_name:
            player.display_name = display_name 
            player.save()

        # 確保玩家統計資料存在
        # 避免循環調用，導入放在方法內部
        from database.player_statistic import PlayerStatistic
        PlayerStatistic.get_or_create(player=player)

        return player

    @staticmethod
    def _get_required_exp(level: int) -> int:
        return int(100 * (level ** 1.5) + level * 20)

    def add_experience(self, amount: int):
        self.experience += amount
        
        is_levelup = False
        while self.experience >= self._get_required_exp(self.level):
            self.experience -= self._get_required_exp(self.level)
            self.level += 1
            is_levelup = True

        if is_levelup:
            Context.bot.dispatch("levelup", self.display_name, "活躍度", self.level)

        self.save()
 
    def add_currency(self, amount: int):
        """增加貨幣數量"""
        self.currency += amount
        self.save()
    
    def remove_currency(self, amount: int):
        """減少貨幣數量"""
        self.currency -= amount
        self.save()

    def set_location(self, location: str):
        """設置玩家當前所在位置"""
        self.location = location
        self.save()

    def add_item(self, item_id: str, quantity: int = 1) -> int:
        """增加物品數量"""
        from database.inventory import Inventory  # 避免循環導入
        return Inventory.add_item(self.id, item_id, quantity)
    
    def remove_item(self, item_id: str, quantity: int = 1) -> dict:
        """減少物品數量"""
        from database.inventory import Inventory  # 避免循環導入
        return Inventory.remove_item(self.id, item_id, quantity)
    
    def has_item(self, item_id: str, required_quantity: int = 1) -> bool:
        """檢查是否擁有足夠物品數量"""
        from database.inventory import Inventory  # 避免循環導入
        return Inventory.has_item(self.id, item_id, required_quantity)
    
    def save_timestamp_voice(self, timestamp: float):
        """保存語音時間戳記"""
        self.timestamp_voice = timestamp
        self.save()

    def remove_timestamp_voice(self):
        """清除語音時間戳記"""
        self.timestamp_voice = None
        self.save()

def init_player_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Player], safe=True)