from data import REGIONS, ITEMS

region = REGIONS.get("boreal_forest")
print(region)

items = ITEMS.find("equipment")
for item in items:
    print(item.name)