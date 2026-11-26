from peewee import fn

from cores import database, logger
from models import FishStatistic, Player


def record(player_id: int, name: str, count: int = 1, size: float = 1.0) -> bool:
    """
    記錄玩家釣獲指定魚種的累計數量與最大尺寸
    """
    if count <= 0:
        return False

    Player.get_or_create(id=player_id)

    with database.atomic():
        FishStatistic.get_or_create(player=player_id, name=name)

        updated = (FishStatistic
                   .update(
                       count=FishStatistic.count + count,
                       size=fn.MAX(FishStatistic.size, size),
                   )
                   .where(FishStatistic.player == player_id)
                   .where(FishStatistic.name == name)
                   .execute())

    if not updated:
        return False

    logger.debug(f"已記錄玩家 {player_id} 釣獲 {name} x{count}（尺寸：{size}）")
    return True
