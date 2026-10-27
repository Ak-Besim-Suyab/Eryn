import math
from models import Inventory, Player

MAX_ROW = 20

def get_page(player_id: int, page: int, item_ids: list[str] = None) -> tuple[list[Inventory], int, int]:
    """ 取得物品列表並計算要列出的頁數

        - page: 要列出的頁數, 這裡由外部傳入, 物件有預設值 1
        - item_ids: 指定的物品 ID 列表, 未指定 (None) 時將列出所有物品
    """
    Player.get_or_create(id = player_id)

    rows = (Inventory
            .select()
            .where(Inventory.player == player_id)
            .where(Inventory.quantity > 0))

    if item_ids is not None:
        rows = rows.where(Inventory.item_id.in_(item_ids))

    rows = rows.order_by(Inventory.item_id)

    total_pages = max(1, math.ceil(rows.count() / MAX_ROW))
    page = min(max(page, 1), total_pages)

    return list(rows.paginate(page, MAX_ROW)), page, total_pages