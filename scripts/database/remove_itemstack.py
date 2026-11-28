from models import ItemInstance
from models import Inventory

Inventory.delete().where(Inventory.item_id == "wooden_crate", Inventory.player == 1184440057596235817).execute()
Inventory.delete().where(Inventory.item_id == "bass").execute()
ItemInstance.delete().execute()