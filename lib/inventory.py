import math
from models import Inventory, Player, ItemInstance

MAX_ROW = 20

def get_page(page: int, player_id: int, item_ids: list[str] = None) -> tuple[list[Inventory | ItemInstance], int, int]:
    """ *
    返回經過`item_ids`篩選的玩家物品列表`rows(list)`, 當前頁數`page(int)`與總頁數`total_pages(int)`

    頁數`page`與總頁數`total_pages`會經過計算並取得當前頁面的值

    .. page:: 要列出的頁數
    .. player_id:: 玩家`id`
    .. item_ids:: 物品`id`串列, 未指定`None`時將列出所有物品
    """

    Player.get_or_create(id = player_id)

    # 取得可堆疊物品
    rows_stackable = (Inventory
                      .select()
                      .where(Inventory.player == player_id)
                      .where(Inventory.quantity > 0))

    # 取得裝備 (未穿戴, 已穿戴則顯示在裝備欄)
    rows_instance = (ItemInstance
                     .select()
                     .where(ItemInstance.player == player_id)
                     .where(ItemInstance.slot.is_null(True)))

    # 排序 (先查詢傳入的 item_id 列表, 然後以 item_id 排序)
    if item_ids is not None:
        rows_stackable = rows_stackable.where(Inventory.item_id.in_(item_ids)).order_by(Inventory.item_id)
        rows_instance  = rows_instance.where(ItemInstance.item_id.in_(item_ids)).order_by(ItemInstance.item_id)

    # 合併
    rows = list(rows_stackable) + list(rows_instance)

    # 計算頁數
    total_pages = max(1, math.ceil(len(rows) / MAX_ROW))
    page = min(max(page, 1), total_pages)

    # 取得指定頁數的物品
    #
    # rows[0:20] 為第一頁
    # rows[20:40] 為第二頁, 以此類推
    #
    start = (MAX_ROW * (page - 1))
    return rows[start:start + MAX_ROW], page, total_pages

