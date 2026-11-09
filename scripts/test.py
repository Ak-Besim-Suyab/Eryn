from data import ITEMS

tags = "equipment:chest:cloth"

t = tags.split(":")

print(t)

items = ITEMS.find_tags(*t)

if items:
    for i in items:
        print(i.name)
else:
    print("None")