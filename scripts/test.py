import data
from data.schema import ItemOpenAction

item = data.item.get("wood_crate")

print(item)
print(item.has_action(ItemOpenAction))