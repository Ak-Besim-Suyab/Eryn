from peewee import *
from database.generic import db

class Player(Model):
    # discord user id
    id = IntegerField(primary_key=True)  

    display_name = TextField(default="Unknown")
    currency_yab = IntegerField(default=0)

    location = TextField(default="Unknown")
    
    card = TextField(null=True)
    use_pet = IntegerField(default=0)

    class Meta:
        database = db


    @classmethod
    def get_or_create_player(cls, user_id: int):
        """獲取或創建玩家"""
        player, created = cls.get_or_create(id=user_id)
        return player

    @property
    def currency(self) -> int:
        """獲取玩家貨幣數量"""
        return self.currency_yab
    
    def add_currency(self, amount: int) -> int:
        """增加貨幣數量"""
        self.currency_yab += amount
        self.save()
    
    def remove_currency(self, amount: int) -> int:
        """減少貨幣數量"""
        self.currency_yab -= amount
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

def init_player_database():
    """初始化玩家數據庫表"""
    with db:
        db.create_tables([Player], safe=True)