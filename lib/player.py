from cores import logger
from cores import database

from models import Player, ItemInstance, Statistic, Material, Currency

from lib import item as itemlib
from lib import material

from data import MATERIALS, LOOT_TABLES, ITEMS
from data.schema.type import ItemType
from data.schema import Item

def get(player_id: int) -> Player:
    """ 
    取得玩家
    """
    player, _ = Player.get_or_create(id = player_id)
    return player

def get_statistic(player_id: int) -> Statistic:
    """
    取得玩家統計資料
    """
    statistic, _ = Statistic.get_or_create(player = player_id)
    return statistic

def get_currency(player_id: int) -> Currency:
    """
    取得玩家通貨
    """
    currency, _ = Currency.get_or_create(player = player_id)
    return currency

def get_material(player_id: int) -> Material:
    """
    取得玩家材料
    """
    mat, _ = Material.get_or_create(player = player_id)
    return mat

def get_region(player_id: int) -> str:
    """
    取得玩家所在地區
    """
    player, _ = Player.get_or_create(id=player_id)
    return player.region

def get_race(player_id: int):
    """
    取得玩家種族
    """
    player, _ = Player.get_or_create(id=player_id)
    return player.race

def get_experience_requirement(level: int) -> float:
    """
    取得指定等級所需經驗值
    """
    base = 100
    exponent = 1.5
    addition = 20
    return round(base * (level ** exponent) + level * addition, 1)

def add_experience(player_id: int, amount: int | float):
    """
    增加玩家經驗值並檢查是否符合升級條件
    """
    if amount < 0:
        raise ValueError("經驗值不可為負數")

    if amount == 0:
        return

    with database.atomic():
        Player.get_or_create(id=player_id)

        updated = (Player
                   .update(experience = Player.experience + amount)
                   .where(Player.id == player_id)
                   .execute())

        if updated:
            level_up(player_id)

def level_up(player_id: int) -> tuple[bool, int]:
    """
    檢查並執行玩家升級，返回 (是否升級, 當前等級)
    """
    upgraded = False

    with database.atomic():
        while True:
            player, _ = Player.get_or_create(id=player_id)
            required = get_experience_requirement(player.level)

            if player.experience < required:
                break

            updated = (Player
                       .update(
                           level      = Player.level + 1,
                           experience = Player.experience - required,
                       )
                       .where(Player.id == player_id)
                       .where(Player.level == player.level)
                       .where(Player.experience >= required)
                       .execute())

            if not updated:
                break

            upgraded = True
            logger.info(f"玩家 {player_id} 升級成功，現在等級為 {player.level + 1}")

        current_level = (Player
                         .select(Player.level)
                         .where(Player.id == player_id)
                         .scalar())

    return upgraded, current_level

def equip(player_id: int, item_id: str, slot: str) -> tuple[bool, str]:
    """ 
    裝備物品到指定欄位, 返回是否成功更改紀錄與對應輸出訊息
    """
    #NOTE: 這裡有個問題, 是否會搜尋到名稱相同的裝備? 需要處理
    instance = ItemInstance.get_or_none(ItemInstance.player == player_id, ItemInstance.item_id == item_id)

    # 沒有任何裝備存在
    if instance is None:
        return False, "找不到物品"

    # 物品已被裝備
    if instance.slot is not None:
        return False, "物品已裝備"

    item = ITEMS.get(item_id)
    component = item.get_component(ItemType.EQUIPMENT) if item else None

    # 沒有可裝備的標籤, 或該物品被定位成不可裝備
    if component is None or component.slot is None:
        return False, "物品無法裝備"

    # 物品槽位與指定槽位不符
    #NOTE: 之後在選取時可能就會直接過濾掉不可裝備的欄位, 目前保留檢查
    if slot != component.slot:
        return False, "物品無法裝備到該欄位"

    with database.atomic():
        # 尋找可裝備的物品
        instance = (ItemInstance
                    .select()
                    .where(ItemInstance.player == player_id,
                           ItemInstance.item_id == item_id,
                           ItemInstance.slot.is_null(True))
                    .order_by(ItemInstance.id)
                    .first())
        if instance is None:
            return False, "找不到可裝備的物品"
        
        # 卸下舊裝備
        (ItemInstance
        .update(slot=None)
        .where(ItemInstance.player == player_id, ItemInstance.slot == slot)
        .execute())

        # 穿上裝備
        (ItemInstance
        .update(slot=slot)
        .where(ItemInstance.id == instance.id)
        .execute())

    return True, "成功裝備"

def unequip(player_id: int, slot: str) -> bool:
    """ 移除指定欄位的物品，返回是否成功移除該筆紀錄
    """
    with database.atomic():
        deleted = (ItemInstance
                   .update(slot=None)
                   .where(
                       ItemInstance.player == player_id, 
                       ItemInstance.slot == slot, 
                       ItemInstance.slot.is_null(False))
                    .execute())

    return deleted > 0

def get_equipped(player_id: int, slot: str) -> ItemInstance | None:
    """
    返回指定裝備欄位的物品
    """
    return (ItemInstance
            .select()
            .where(ItemInstance.player == player_id, 
                   ItemInstance.slot == slot)
            .first())

def get_equipments(player_id: int, unequipped: bool = True) -> list[ItemInstance] | None:
    """
    返回裝備欄, `equipped` 為 `True` 代表已裝備, `False` 代表未裝備
    """
    rows = (ItemInstance
            .select()
            .where(ItemInstance.player == player_id)
            .where(ItemInstance.slot.is_null(unequipped)))
    return list(rows)

def is_equipped(player_id: int, slot: str) -> bool:
    return get_equipped(player_id, slot) is not None

def open_item(player_id: int, item: Item, times: int = 1) -> tuple[bool, dict]:

    loot = item.get_component(ItemType.LOOT)
    if loot is None:
        return False, None

    # NOTE: 這裡先實作簡易邏輯，之後如果讓 loot_table 可以有多個，則需要再做調整
    loot_table = LOOT_TABLES.get(loot.loot_tables[0])
    if loot_table is None:
        logger.warning(f"找不到物品 {item.id} 的掉落表 {loot.loot_tables[0]}")
        return False, None

    looted = loot_table.roll(times)

    item_lines = []
    for (loot_type, loot_id), quantity in looted.items():
        match loot_type:
            case "material" | "resource":
                mat = MATERIALS.get(loot_id)
                material.give(player_id, loot_id, quantity)
                # NOTE: 這裡之後改成 description.append(material.get_line(item_id, quantity))
                item_lines.append(f"- {mat.icon}{mat.name} {quantity}")
            case _:
                pass

    itemlib.remove(player_id, item.id, times)

    return True, item_lines

def get_timestamp_daily(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_daily

def set_timestamp_daily(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_daily = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的每日時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的每日時間戳記")

def get_timestamp_voice(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_voice

def set_timestamp_voice(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_voice = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的語音時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的語音時間戳記")