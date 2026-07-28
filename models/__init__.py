from .button import *
from .dialogue import *
from .embed import *
from .image import *
from .query import *
from .role import *
from .select import *
from .view import *
from .player import *
from .statistic import *

def init_database():
    player.init()
    init_statistic_database()