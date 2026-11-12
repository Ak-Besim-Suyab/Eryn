from data import BUILDINGS

from peewee import fn

from cores.database import database
from cores.logger import logger

from models import Building
from models import Contribution
from models import Resource

from lib import resource

def add_contribution(
        player_id: int,
        building_id: str,
        resource_id: str,
        quantity: int) -> tuple:

    """
    增加建築的資源貢獻
    """
    
    Building.get_or_create(id=building_id)

    with database.atomic():

        contribution, _ = Contribution.get_or_create(building=building_id, player=player_id)

        # 檢查資源類別是否存在
        if not hasattr(contribution, resource_id):
            raise ValueError(f"錯誤，未知的資源 {resource_id}")

        res, _ = Resource.get_or_create(player=player_id)

        # 檢查玩家資源數量
        if getattr(res, resource) < quantity:
            return False, "資源不足"
        
        # 移除玩家資源數量
        # NOTE: 這裡回傳的資訊是臨時的，請記得補全正確回傳資訊
        success = resource.remove(player_id, resource_id, quantity)
        if not success:
            return False, "扣除資源時發生錯誤"

        # 增加建築物貢獻值
        (Contribution
            .update(**{resource: getattr(Contribution, resource) + quantity})
            .where(Contribution.id == contribution.id)
            .execute())

        logger.debug(f"成功給予 {player_id} {quantity} 個 {resource} 到 {building_id}")

    return True, "成功"

def get_building_contributions(building_id: str) -> dict[str, int]:
    """
    取得指定建築的所有資源貢獻值總和
    """
    resources = ["wood", "stone", "food"]

    sum = [
        fn.COALESCE( fn.SUM(getattr(Contribution, resource)), 0 ).alias(resource)
        for resource in resources
    ]

    rows = (Contribution
        .select(*sum)
        .where(Contribution.building == building_id)
        .dicts()
        .get()
    )

    return rows

def can_upgrade(current_resources: dict, required_resources: dict) -> bool:
    return all(current_resources.get(resource, 0) >= required for resource, required in required_resources.items())

def upgrade(building_id: str) -> tuple[bool, int]:
    """ 嘗試升級建築，返回 `upgraded: bool` 表示升級與否和 `level: int` 表示當前等級
    """
    data = BUILDINGS.get(building_id)

    upgrade = False
    with database.atomic():

        building: Building
        building, _ = Building.get_or_create(id=building_id)

        current = get_building_contributions(building_id)

        while True:
            required = data.get_leveling_conditions(building.level)
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