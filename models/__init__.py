from data.schema.button import *
from data.schema.select import *

# -----------------------------------------------------------
from cores.database import database

from .player import Player, Attribute
from .skill import *
from .inventory import *
from .item_instance import *
from .item_affix import *
from .material import *
from .currency import *
from .building import *
from .contribution import *
from .house import *
from .statistic import *

def init_databases():
    with database:
        database.create_tables(
            [
                Player, 
                Attribute,
                Skill,
                Currency,
                Material, 
                Inventory,
                ItemInstance,
                ItemAffix,
                Building,
                Contribution,
                House, 
                Statistic,
                FishStatistic,
            ], 
            safe=True)