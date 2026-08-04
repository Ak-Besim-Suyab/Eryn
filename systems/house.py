from models import Player
from models import House
from database import db

class HouseSystem:

    @staticmethod
    def register(channel_id: int, player_id: int) -> tuple[House, bool]:

        """這個方法用於註冊小屋頻道, 並綁定玩家, 返回 tuple[House, bool], 這裡的布林值表示是否為新建"""

        Player.get_or_create(id=player_id)

        with db.atomic():
            house, created = House.get_or_create(id=channel_id, defaults={'owner': player_id})

        return house, created

    @staticmethod
    def delete(channel_id: int):

        with db.atomic():
            house = House.get_or_none(id=channel_id)
            if house is None:
                return False

            house.delete_instance()
            return True

# -----------------------------------------------------------
# 創建單例
# -----------------------------------------------------------
_instance = HouseSystem()

register = _instance.register
delete = _instance.delete