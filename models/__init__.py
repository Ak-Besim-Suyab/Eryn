from data.schema.button import *
from .embed import *
from .query import *
from data.schema.select import *
from .view import *

# -----------------------------------------------------------
from database import db

from .player import *
from .house import *
from .statistic import *

def init_databases():
    with db:
        db.create_tables([Player, House, Statistic], safe=True)