from peewee import fn

from cores.database import database
from cores.logger import logger

from models import Player
from models import Building
from models import Contribution

from lib.utils import file

def add_experience(build_id: str, amount: int) -> None:
    with database.atomic():
        (Building
            .update(experience=Building.experience + amount)
            .where(Building.id == build_id)
            .execute())

def add_contribution(player_id: int, build_id: str, resource: str, quantity: int = 1) -> None:

    Player.get_or_create(id=player_id)
    Building.get_or_create(id=build_id)

    with database.atomic():

        contribution, _ = Contribution.get_or_create(building=build_id, player=player_id)

        (Contribution
            .update(**{resource: getattr(Contribution, resource) + quantity})
            .where(Contribution.id == contribution.id)
            .execute())

        logger.debug(f"成功給予 {player_id} {quantity} 個 {resource} 到 {build_id}")

def get_building_contributions(build_id: str) -> dict[str, int]:
    """ 取得指定建築的所有資源貢獻值總和
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