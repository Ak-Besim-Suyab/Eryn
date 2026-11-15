from peewee import fn

from cores.database import database
from cores.logger import logger

from models import Building
from models import Contribution

from lib import resource

def add_contribution(
        player_id: int, 
        building_id: str, 
        resource_id: str, 
        quantity: int) -> tuple[bool, str]:
    
    """
    增加建築的資源貢獻同時移除玩家資源, 返回是否成功與訊息
    """

    # 確保貢獻與建築物資料存在
    Building.get_or_create(id=building_id)
    Contribution.get_or_create(building=building_id, player=player_id)

    with database.atomic():

        # 移除玩家資源, 參數合法性, 資源數量都交由資源模組處理, 這裡只負責接收是否成功
        success, msg = resource.remove(player_id, resource_id, quantity)

        if not success:
            return False, msg

        # 增加建築物貢獻值, 需要查詢兩個外鍵, 否則會變成增加所有建築物或所有玩家指定欄位上的值
        (Contribution
            .update(**{resource_id: getattr(Contribution, resource_id) + quantity})
            .where(Contribution.building == building_id)
            .where(Contribution.player   == player_id)
            .execute())

    logger.debug(f"成功給予 {player_id} {quantity} 個 {resource_id} 到 {building_id}")
    return True, "成功"

def get_contribution(building_id: str, resource: str) -> dict[str, int]:
    """
    取得單位指定資源貢獻值總和，返回字典：資源名稱為 key, 總數為 value
    """
    sum = fn.COALESCE(fn.SUM(getattr(Contribution, resource)), 0).alias(resource)

    contribution = (Contribution
                    .select(sum)
                    .where(Contribution.building == building_id)
                    .dicts()
                    .get())

    return contribution

def get_contributions(building_id: str) -> dict[str, int]:
    """
    取得建築的所有資源貢獻值總和, 返回資源名稱為鍵, 總數為值的字典
    """
    resources = ["wood", "stone", "food", "iron"]

    sum = [
        fn.COALESCE(fn.SUM(getattr(Contribution, resource)), 0).alias(resource)
        for resource in resources]

    rows = (Contribution
        .select(*sum)
        .where(Contribution.building == building_id)
        .dicts()
        .get())

    return rows

def get_required_resources(level: int,
                           base: int = 1350,
                           init: float = 2.0,
                           ceil: float = 4.0,
                           multiplier: float = 0.95) -> int:

    """
    資源數量預設計算公式：
    scaling = ceil - (ceil - init) * (multiplier ** (level - 1))

    .. level:: 為傳入值, 為乘區指數
    .. base:: 基礎值, 受倍率公式影響後產出最終值
    .. init:: 初始倍率, 代指預期天數, 倍率公式會嘗試將此值與最大倍率得差值, 並使差值逼近於 0
    .. ceil:: 最大倍率, 代指預期天數, 倍率公式的結果會逼近此值, 但不會超過
    .. multiplier:: 乘區, 預設小於 1, 以等級為指數, 等級越大時將會逼近於 0
    """

    scaling = ceil - (ceil - init) * (multiplier ** (level - 1))

    return round(base * scaling / 10) * 10

def get_resource_level(build_id: str, resource: str) -> int:
    pass

# 因為更改了資源總量對於等級的計算模式，所以這個函數不再使用了，之後要更換成建築物本體的經驗值模式或刪除
def can_upgrade(current: dict, required: dict) -> bool:
    """
    判定是否升級, 需要傳入當前資料與條件資料的字典, 返回是否完全符合
    """
    return all(current.get(resource, 0) >= quantity for resource, quantity in required.items())

def upgrade(building_id: str) -> tuple[bool, int]:
    """ 
    升級建築，返回`upgraded: bool`表示升級與否和`level: int`表示當前等級
    """
    upgrade = False
    with database.atomic():

        building: Building
        building, _ = Building.get_or_create(id=building_id)

        current = get_contributions(building_id)

        while True:
            # NOTE: 這裡移除了原本的函數，要改
            required = 0
            # check if max level.
            if required is None:
                break

            # check if enough resource.
            if not can_upgrade(current, required):
                break

            updated = (Building
                .update(level=Building.level + 1)
                .where(Building.id == building_id, Building.level == building.level)
                .execute()
            )

            # check if upgrade success, prevent race condition.
            if not updated:
                break

            building.level += 1
            upgrade = True

    return upgrade, building.level