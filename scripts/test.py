from lib.entity import building

total = 0
for i in range(1, 100):
    req = building.get_required_resources(i)
    total += req
    print(i, req, total)