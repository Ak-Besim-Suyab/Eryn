import data

building = data.building.get("sanctuary")

conditions = building.get_leveling_conditions(5)

print(conditions)