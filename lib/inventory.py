import math
from data import ITEMS, RACES

from model import Player
from model import Inventory
from model import ItemInstance

from lib import player
from lib import item

def get_page(page: int, player_id: int, item_ids: list[str] = None) -> tuple[list[Inventory | ItemInstance], int, int]:
    """ *
    返回經過`item_ids`篩選的玩家物品列表`rows(list)`, 當前頁數`page(int)`與總頁數`total_pages(int)`

    頁數`page`與總頁數`total_pages`會經過計算並取得當前頁面的值

    .. page:: 要列出的頁數
    .. player_id:: 玩家`id`
    .. item_ids:: 物品`id`串列, 未指定`None`時將列出所有物品
    """
    # 最大行數 (不可變動)
    MAX_ITEM_ROW = 10

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

    # 如果有傳入分類, 則將查詢縮限到分類以內
    if item_ids is not None:
        rows_stackable = rows_stackable.where(Inventory.item_id.in_(item_ids)).order_by(Inventory.item_id)
        rows_instance  = rows_instance.where(ItemInstance.item_id.in_(item_ids)).order_by(ItemInstance.item_id)

    # 合併
    rows = list(rows_stackable) + list(rows_instance)
    rows.sort(key=item.sort_key)

    return _page_caculated(rows, page, MAX_ITEM_ROW)

def get_equip_page(page: int, player_id: int) -> tuple[list[tuple[str, str | None]], int, int]:
    """
    返回經過欄位匹配後的裝備列表`rows(list)`, 當前頁數`page(int)`與總頁數`total_pages(int)`
    """
    # 最大行數
    MAX_EQUIP_ROW = 10

    Player.get_or_create(id = player_id)

    # 取得所有裝備中的物品
    rows = player.get_equipments(player_id=player_id, unequipped=False)

    # 根據裝備順序重新排序
    rows.sort(key=item.equip_sort_key)
    rows = {row.slot: ITEMS.get(row.item_id).name for row in rows}

    # 取得所有可裝備欄位
    # NOTE: 之後補上其他來源的欄位
    race = RACES.get(player.get_race(player_id))

    # 匹配欄位
    slot_rows = [(slot, rows.get(slot, None)) for slot in race.slots]

    return _page_caculated(slot_rows, page, MAX_EQUIP_ROW)

def _page_caculated(rows: list, page: int, max_row: int):
    """
    返回根據最大行數計算後的指定分頁串列, 當前頁數與總頁數 (最大頁數會向上取整以避免缺頁)
    """
    # 計算當前頁數與總頁數
    total_pages = max(1, math.ceil(len(rows) / max_row))
    page = min(max(page, 1), total_pages)

    # 取得指定頁數的物品, rows[0:20] 為第一頁, rows[20:40] 為第二頁, 以此類推
    start = (max_row * (page - 1))
    return rows[start:start + max_row], page, total_pages