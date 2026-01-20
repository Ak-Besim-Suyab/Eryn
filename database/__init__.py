"""
数据库初始化模块

这个文件负责：
1. 导入所有数据库模型和初始化函数
2. 按正确的顺序初始化表
3. 提供统一的初始化入口

初始化顺序的重要性：
  Player 表必须先创建
  └─ 其他表通过 ForeignKeyField 依赖 Player

使用方式：
  from database import init_all_databases
  init_all_databases()
"""

from database.player import init_player_database
from database.dummy import init_dummy_database
from database.affection import init_affection_database
from database.character import init_character_database
from database.skill import init_skill_database
from database.inventory import init_inventory_database


def init_all_databases():
    """
    初始化所有數據庫表
    
    按照依賴關係的正確順序初始化：
    1. Player（核心表）
    2. Dummy（獨立表）
    3. Affection（依賴 Player 和 Dummy）
    4. Character（依賴 Player - 角色等級）
    5. Skill（依賴 Player - 技能等級）
    
    這個函數確保了無論在哪裡調用，初始化流程都是一致的。
    """
    print("[Database] 正在初始化數據庫...")
    
    # 1. 核心表 - Player 必須第一個創建
    init_player_database()
    print("[Database] ✅ Player 表已初始化")
    
    # 2. 獨立表
    init_dummy_database()
    print("[Database] ✅ Dummy 表已初始化")
    
    # 3. 關聯表（依賴 Player 和 Dummy）
    init_affection_database()
    print("[Database] ✅ Affection 表已初始化")
    
    # 4. 角色等級表（依賴 Player）
    init_character_database()
    print("[Database] ✅ Character 表已初始化")
    
    # 5. 技能等級表（依賴 Player）
    init_skill_database()
    print("[Database] ✅ Skill 表已初始化")
    
    # 6. 背包系統表（依賴 Player）
    init_inventory_database()
    print("[Database] ✅ Inventory 表已初始化")
    
    print("[Database] ✅ 所有表初始化完成！")


__all__ = ['init_all_databases']
