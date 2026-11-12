from cores import database
from cores import logger

from models import Player
from models import Resource

def give(player_id: int, resource_id: str, quantity: int) -> bool:
    """
    給予玩家指定資源, 回傳是否成功通過資料庫更新
    """
    # 驗證參數合法性, 若不合法則直接回傳 False
    if not valid(resource_id, quantity):
        return False

    Player.get_or_create(id = player_id)
    Resource.get_or_create(player = player_id)

    with database.atomic():
        (Resource
        .update(**{resource_id: getattr(Resource, resource_id) + quantity})
        .where(Resource.player == player_id)
        .execute())

    logger.debug(f"成功給予 {player_id} {quantity} 個 {resource_id}")

    return True
    
def remove(player_id: int, resource_id: str, quantity: int) -> bool:
    """
    移除玩家指定資源, 回傳是否成功通過資料庫更新
    """
    # 驗證參數合法性, 若不合法則直接回傳 False
    if not valid(resource_id, quantity):
        return False

    # 更新資料庫, 查詢條件包含數量驗證
    with database.atomic():
        updated = (Resource
                   .update(**{resource_id: getattr(Resource, resource_id) - quantity})
                   .where(Resource.player == player_id, getattr(Resource, resource_id) >= quantity)
                   .execute())

    # 沒有資料庫更新紀錄 (updated = 0) 返回 False
    if not updated: 
        logger.debug(f"玩家 {player_id} {resource_id} 不足，無法扣除 ({quantity})")
        return False

    logger.debug(f"成功消耗 {player_id} {quantity} 個 {resource_id}")
    return True

def valid(resource_id: str, quantity: int) -> bool:

    # 檢查資源是否為空, 或不存在於資料庫欄位
    if not resource_id or resource_id not in Resource._meta.fields:
        logger.warning(f"出現未定義的資源: {resource_id}")
        return False

    # 檢查資源數量是否大於零
    if quantity <= 0:
        logger.warning(f"變更的資源數量必須大於零，傳入值為: {quantity}")
        return False

    return True