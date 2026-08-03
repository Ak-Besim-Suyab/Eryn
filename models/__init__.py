from .button import *
from .dialogue import *
from .embed import *
from .image import *
from .query import *
from .role import *
from .select import *
from .view import *

# -----------------------------------------------------------
from database import db

from .player import *
from .house import *
from .statistic import *

def init_databases():
    with db:
        db.create_tables([Player, House, Statistic], safe=True)