import random

from data import REGIONS, LINES

from model import Player

def move(player_id: int, region_name: str):
    # 取得玩家
    player, _ = Player.get_or_create(id=player_id)

    # 取得地圖物件
    r = REGIONS.get(region_name)

    # 如果移動位置與目前所在位置相同，返回失敗與關聯訊息
    if player.region == region_name:
        return False, LINES.get("move_fail").random(region_name=r.name)
    
    Player.update(region=region_name).where(Player.id == player_id).execute()

    return True, "成功到達"    

def get_cost(region_from: str, region_to: str):
    region_from = REGIONS.get(region_from)
    cost = region_from.cost.get(region_to)
    return cost if cost else 5