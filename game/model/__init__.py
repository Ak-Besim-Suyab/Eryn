from .inventory import *
from .item import *
from models import player
from .shop import *
from models.statistic import init_statistic_database, Statistic

def init_all_databases():
    """
    初始化所有數據庫表
    """
    print("[Database] 正在初始化數據庫...")
    
    # 1. 核心表 - Player 必須第一個創建
    player.init()
    print("[Database] ✅ Player 表已初始化")

    # 2. 統計表 - 依賴 Player ID
    init_statistic_database()
    print("[Database] ✅ Statistic 表已初始化")
    
    # 6. 背包系統表（依賴 Player）
    init_inventory_database()
    print("[Database] ✅ Inventory 表已初始化")
    
    print("[Database] ✅ 所有表初始化完成！")

__all__ = ['init_all_databases']