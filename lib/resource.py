from typing import Optional

from cores.database import database
from cores.logger import logger

from models import Player
from models import Resource

RESOURCE_NAMES = ["wood", "stone", "food"]

def give(player_id: int, resource: str, quantity: int = 1) -> Optional[Resource]:

    if not valid(resource, quantity):
        return

    Player.get_or_create(id=player_id)
    Resource.get_or_create(player = player_id)

    with database.atomic():
        (Resource
        .update(**{resource: getattr(Resource, resource) + quantity})
        .where(Resource.player == player_id)
        .execute())

    logger.debug(f"成功給予 {player_id} {quantity} 個 {resource}")

    return Resource.get(Resource.player == player_id)
    
def consume(player_id: int, resource: str, quantity: int = 1):
    pass

def valid(resource: str, quantity: int) -> bool:

    # 檢查是否傳入空資源
    if not resource:
        logger.warning("警告，給予的資源為空")
        return False

    if resource not in RESOURCE_NAMES:
        logger.warning(f"警告，未定義的資源: {resource}")
        return False

    if not isinstance(quantity, int) or quantity <= 0:
        logger.warning(f"警告，資源數量必須為正整數: {quantity}")
        return False

    return True