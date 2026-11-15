from models import Contribution

Contribution.get_or_create(building="modelhouse", player=1)
Contribution.get_or_create(building="modelhouse", player=2)
Contribution.get_or_create(building="modelhouse", player=3)

updated = (Contribution
           .update(stone = Contribution.stone + 100)
           .where(Contribution.building == "modelhouse")
           .execute())

print(updated)