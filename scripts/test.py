import data

matchs = data.item.find_flag(openable=True)

for item in matchs:
    print(item.name)