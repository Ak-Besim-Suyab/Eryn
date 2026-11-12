import random

from data import REGIONS, LINES

from models import Player

def move(player_id: int, region: str) -> tuple[bool, str]:
    # 取得玩家
    player, _ = Player.get_or_create(id=player_id)

    # 取得地圖物件
    reg = REGIONS.get(region)

    # 如果移動位置與目前所在位置相同，返回失敗與關聯訊息
    if player.region == region:
        line = (LINES
                .get("move_fail")
                .random(region_name=reg.name))
        return False, line

    # 更新玩家地圖位置
    (Player
     .update(region=region)
     .where(Player.id == player_id)
     .execute())

    return True, "成功到達"    

def get_cost(region_from: str, region_to: str) -> int:
    reg = REGIONS.get(region_from)
    cost = reg.cost.get(region_to)
    return cost if cost else 15