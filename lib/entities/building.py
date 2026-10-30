
from cores.database import database
from models import Building
from models import Contribution

def add_experience(build_id: str, amount: int) -> None:
    with database.atomic():
        (Building
            .update(experience=Building.experience + amount)
            .where(Building.id == build_id)
            .execute())

def add_contribution(player_id: int, build_id: str, resource: str, quantity: int = 1) -> None:

    Building.get_or_create(id=build_id)

    with database.atomic():
        (Contribution
            .update(**{resource: getattr(Building, resource) + quantity})
            .where(Contribution.building == build_id, Contribution.player == player_id)
            .execute())