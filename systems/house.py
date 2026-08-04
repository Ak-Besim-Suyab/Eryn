from models import Player
from models import House
from database import db

"""
    這個模塊用於實作 house model 的業務邏輯, 僅負責運行與輸出結果, 訊息輸出由 cogs 或更外層的邏輯負責

    :: register
        這個方法用於將小屋頻道紀錄至資料庫, 並綁定玩家, 返回 tuple[House, bool], 這裡的布林值表示是否為新建
        這裡使用 get_or_create 方法, 若頻道已經存在, 將不會再次建立, 而是返回已存在的紀錄與布林值
    
    :: delete
        這個方法用於刪除小屋頻道紀錄, 返回布林值表示是否成功刪除
        這裡使用 get_or_none 方法, 若頻道不存在, 將返回 None, 並以此判斷 False 表示刪除失敗
"""

class HouseSystem:

    @staticmethod
    def register(channel_id: int, player_id: int) -> tuple[House, bool]:

        Player.get_or_create(id=player_id)

        with db.atomic():
            house, created = House.get_or_create(id=channel_id, defaults={'owner': player_id})

        return house, created

    @staticmethod
    def delete(channel_id: int) -> bool:

        with db.atomic():
            house = House.get_or_none(id=channel_id)
            if house is None:
                return False

            house.delete_instance()
            return True

    @staticmethod
    def get_owners() -> set[int]:
        """返回 House 資料內的 owner_id 欄位"""
        return {house.owner.id for house in House.select(House.owner)}

    @staticmethod
    def get_houses() -> set[int]:
        """返回 House 資料內的 id 欄位"""
        return {house.id for house in House.select(House.id)}

# -----------------------------------------------------------
# 創建單例
# -----------------------------------------------------------
_instance = HouseSystem()

register = _instance.register
delete = _instance.delete
get_owners = _instance.get_owners
get_houses = _instance.get_houses