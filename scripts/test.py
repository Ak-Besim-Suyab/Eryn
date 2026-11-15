from lib.entity import building

contr = building.get_contributions("modelhouse")
print(contr)

contr = building.get_contributions("sanctuary")
print(contr)
