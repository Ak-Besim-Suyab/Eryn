import data

building = data.building.get("sanctuary")

for condition in building.level_conditions:
    print(condition.level, condition.wood, condition.stone, condition.food)