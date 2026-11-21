from models import Currency
from cores import logger

def get(player_id: int, currency: str) -> int:
    """
    取得玩家的通貨資料
    """
    Currency.get_or_create(player = player_id)

    return (Currency
            .select(getattr(Currency, currency))
            .where(Currency.player == player_id)
            .scalar())

def give(player_id: int, currency: str, quantity: int) -> bool:

    if quantity < 0:
        return False

    Currency.get_or_create(player = player_id)

    (Currency
     .update(**{currency: getattr(Currency, currency) + quantity})
     .where(Currency.player == player_id)
     .execute())

    logger.debug(f"成功給予 {player_id} {quantity} {currency}.")

    return True