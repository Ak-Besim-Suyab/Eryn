from cores.database import database
from cores.logger import logger

from models import Player
from models import Resource

RESOURCE_NAMES = ["wood", "stone", "food"]

def is_valid(resources: dict[str, int]) -> bool:

    # 檢查是否傳入空資源
    if not resources:
        logger.warning("警告，給予的資源為空")
        return False

    # 檢查是否傳入正確名稱與數量的資源
    for name, quantity in resources.items():
        if name not in RESOURCE_NAMES:
            logger.warning(f"警告，未定義的資源: {name}")
            return False
        if not isinstance(quantity, int) or quantity <= 0:
            logger.warning(f"警告，資源數量必須為正整數: {quantity}")
            return False

    return True

def give(player_id: int, **resources) -> Resource:

    if not is_valid(resources):
        return

    Player.get_or_create(id=player_id)
    resource, _ = Resource.get_or_create(player = player_id)

    with database.atomic():
        (Resource
        .update(**{name: getattr(Resource, name) + quantity for name, quantity in resources.items()})
        .where(Resource.player == player_id)
        .execute())

    logger.debug(f"成功給予 {player_id} 資源: {resources}")
    return Resource.get_by_id(player_id)
    
def consume(player_id: int, **resources):

    if not is_valid(resources):
        return