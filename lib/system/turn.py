from models import Player

def add(player_id: int, amount: int):

    # 檢查數量是否為正整數
    if amount < 0:
        return False

    Player.get_or_create(id = player_id)

    updated = (Player
               .update(turn = Player.turn + amount)
               .where(Player.id == player_id)
               .execute())

    # 檢查是否成功更新資料
    if not updated:
        return False

    return True