from .button import *
from .embed import *
from .inventory import *
from .item import *
from .message import *
from .player import *
from .query import *
from .select import *
from .shop import *
from .view import *

def init_all_databases():
    """
    初始化所有數據庫表
    """
    print("[Database] 正在初始化數據庫...")
    
    # 1. 核心表 - Player 必須第一個創建
    init_player_database()
    print("[Database] ✅ Player 表已初始化")
    
    # 6. 背包系統表（依賴 Player）
    init_inventory_database()
    print("[Database] ✅ Inventory 表已初始化")
    
    print("[Database] ✅ 所有表初始化完成！")

__all__ = ['init_all_databases']