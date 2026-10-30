from data.schema.button import *
from data.schema.select import *

# -----------------------------------------------------------
from cores.database import database

from .player import *
from .inventory import *
from .resource import *
from .building import *
from .contribution import *
from .house import *
from .statistic import *

def init_databases():
    with database:
        database.create_tables([
            Player, 
            Inventory, 
            Resource, 
            Building,
            Contribution,
            House, 
            Statistic,], safe=True)