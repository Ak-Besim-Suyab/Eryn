import data as registry

from peewee import fn

from cores.database import database
from cores.logger import logger

from models import Player
from models import Building
from models import Contribution

def add_contribution(player_id: int, build_id: str, resource: str, quantity: int = 1) -> tuple[bool, int]:
    """
    增加建築的資源貢獻，並計算增加後是否升級，返回 `upgraded: bool` 表示升級與否和 `level: int` 表示當前等級
    """
    Player.get_or_create(id=player_id)
    building, _ = Building.get_or_create(id=build_id)

    with database.atomic():

        contribution, _ = Contribution.get_or_create(building=build_id, player=player_id)

        (Contribution
            .update(**{resource: getattr(Contribution, resource) + quantity})
            .where(Contribution.id == contribution.id)
            .execute())

        logger.debug(f"成功給予 {player_id} {quantity} 個 {resource} 到 {build_id}")

    # try upgrade.
    upgraded, level = upgrade(build_id)
    return upgraded, level

def get_building_contributions(build_id: str) -> dict[str, int]:
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
        .where(Contribution.building == build_id)
        .dicts()
        .get()
    )

    return rows

def can_upgrade(current_resources: dict, required_resources: dict) -> bool:
    return all(current_resources.get(resource, 0) >= required for resource, required in required_resources.items())

def upgrade(building_id: str) -> tuple[bool, int]:
    """ 嘗試升級建築，返回 `upgraded: bool` 表示升級與否和 `level: int` 表示當前等級
    """
    data = registry.building.get(building_id)

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