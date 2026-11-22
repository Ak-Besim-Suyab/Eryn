from cores import database
from cores import logger

from models import Player
from models import Material

from data import MATERIALS
from data.enums import MaterialName

def get(player_id: int, material: str) -> int:

    Player.get_or_create(id = player_id)
    Material.get_or_create(player = player_id)

    if material not in MaterialName:
        raise ValueError(f"unknown material name: {material}")

    return (Material
            .select(getattr(Material, material))
            .where(Material.player == player_id)
            .scalar())

def give(player_id: int, material_id: str, quantity: int) -> bool:
    """
    給予玩家指定材料, 回傳是否成功通過資料庫更新
    """
    # 驗證參數合法性, 若不合法則直接回傳 False
    if not is_valid(material_id, quantity):
        return False

    Player.get_or_create(id = player_id)
    Material.get_or_create(player = player_id)

    with database.atomic():
        updated = (Material
                   .update(**{material_id: getattr(Material, material_id) + quantity})
                   .where(Material.player == player_id)
                   .execute())

        if not updated:
            return False

    logger.debug(f"成功給予 {player_id} {quantity} {material_id}.")

    return True
    
def remove(player_id: int, material_id: str, quantity: int) -> tuple[bool, str]:
    """
    移除玩家材料, 驗證參數與移除數量是否合法, 回傳是否成功通過資料庫更新
    """
    # 驗證參數合法性, 若不合法則直接回傳 False
    if not is_valid(material_id, quantity):
        return False, ""

    # 更新資料庫, 查詢條件包含數量驗證
    with database.atomic():
        updated = (Material
                   .update(**{material_id: getattr(Material, material_id) - quantity})
                   .where(Material.player == player_id, getattr(Material, material_id) >= quantity)
                   .execute())

    # 沒有資料庫更新紀錄 (updated = 0) 返回 False
    if not updated: 
        logger.debug(f"玩家 {player_id} {material_id} 不足，無法扣除 ({quantity})")
        return False, "你的材料已不足以扣除。"

    logger.debug(f"成功消耗 {player_id} {quantity} 個 {material_id}")
    return True, ""

def is_valid(material_id: str, quantity: int = 0) -> bool:
    """
    驗證材料參數是否合法
    """
    if material_id not in MATERIALS:
        logger.warning(f"出現未定義的材料: {material_id}")
        return False

    if material_id not in Material._meta.fields:
        logger.warning(f"出現不符合資料庫欄位的材料: {material_id}")
        return False

    if quantity < 0:
        logger.warning(f"變更的材料數量必須大於零，傳入值為: {quantity}")
        return False

    return True
