from .player import *
from .statistic import *
from .dummy import *
from .affection import *
from .skill import *
from .inventory import *
from .message import *
from .status import *
from .guild import *


def init_all_databases():
    """
    初始化所有數據庫表
    """
    print("[Database] 正在初始化數據庫...")
    
    # 1. 核心表 - Player 必須第一個創建
    init_player_database()
    print("[Database] ✅ Player 表已初始化")

    init_statistic_database()
    print("[Database] ✅ Statistic 表已初始化")
    
    # 2. 獨立表
    init_dummy_database()
    print("[Database] ✅ Dummy 表已初始化")
    
    # 3. 關聯表（依賴 Player 和 Dummy）
    init_affection_database()
    print("[Database] ✅ Affection 表已初始化")
    
    # 4. 技能等級表（依賴 Player）
    init_skill_database()
    print("[Database] ✅ Skill 表已初始化")

    init_status_database()
    print("[Database] ✅ Status 表已初始化")
    
    # 6. 背包系統表（依賴 Player）
    init_inventory_database()
    print("[Database] ✅ Inventory 表已初始化")

    init_guild_database()
    print("[Database] ✅ Guild 表已初始化")
    
    print("[Database] ✅ 所有表初始化完成！")


__all__ = ['init_all_databases']
