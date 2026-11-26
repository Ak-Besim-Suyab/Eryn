from cores import database
from cores import logger

from data.enums import AttributeName
from models import Attribute, Player

def is_valid(attribute_id: str) -> bool:
    """
    驗證屬性欄位名稱是否合法
    """
    if attribute_id not in AttributeName:
        logger.warning(f"出現未定義的屬性名稱: {attribute_id}")
        return False

    if attribute_id not in Attribute._meta.fields:
        logger.warning(f"出現不符合資料庫欄位的屬性: {attribute_id}")
        return False

    return True


def get(player_id: int, attribute_id: str) -> int:
    """
    取得玩家指定屬性的數值
    """
    if not is_valid(attribute_id):
        raise ValueError(f"unknown attribute name: {attribute_id}")

    Player.get_or_create(id=player_id)
    Attribute.get_or_create(player=player_id)

    return (Attribute
            .select(getattr(Attribute, attribute_id))
            .where(Attribute.player == player_id)
            .scalar())


def set(player_id: int, attribute_id: str, value: int) -> bool:
    """
    設定玩家指定屬性的數值，回傳是否成功更新資料庫
    """
    if not is_valid(attribute_id):
        return False

    Player.get_or_create(id=player_id)
    Attribute.get_or_create(player=player_id)

    with database.atomic():
        updated = (Attribute
                   .update(**{attribute_id: value})
                   .where(Attribute.player == player_id)
                   .execute())

    if not updated:
        return False

    logger.debug(f"已將玩家 {player_id} 的 {attribute_id} 設定為 {value}")
    return True
