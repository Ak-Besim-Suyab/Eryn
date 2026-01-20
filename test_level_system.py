#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試 Character 系統的腳本
運行方式：python test_level_system.py
"""

from database import init_all_databases
from database.player import Player
from database.character import Character

def test_level_system():
    print('[测试开始]')
    print()

    # 1. 初始化数据库
    print('1️⃣ 初始化数据库...')
    try:
        init_all_databases()
        print('✅ 数据库初始化成功')
    except Exception as e:
        print(f'❌ 初始化失败：{e}')
        return False

    print()

    # 2. 创建玩家
    print('2️⃣ 创建测试玩家...')
    try:
        player = Player.get_or_create_player(12345)
        print(f'✅ 玩家创建成功：{player.display_name} (ID: {player.id})')
    except Exception as e:
        print(f'❌ 玩家创建失败：{e}')
        return False

    print()

    # 3. 初始化角色等級
    print('3️⃣ 初始化角色等級...')
    try:
        character = Character.get_or_create_character(12345)
        print(f'✅ 角色等級建立：Lv.{character.level}，經驗值：{character.experience}')
    except Exception as e:
        print(f'❌ 等級建立失敗：{e}')
        return False

    print()

    # 4. 測試增加經驗值（不升級）
    print('4️⃣ 測試增加經驗值（50點，不升級）...')
    try:
        result = Character.add_experience(12345, 50)
        print(f'✅ 經驗值增加：')
        print(f'   - 當前等級：Lv.{result["level"]}')
        print(f'   - 當前經驗值：{result["experience"]}')
        print(f'   - 是否升級：{result["leveled_up"]}')
    except Exception as e:
        print(f'❌ 增加經驗值失敗：{e}')
        return False

    print()

    # 5. 測試升級
    print('5️⃣ 測試升級（增加100點，應該升級）...')
    try:
        result = Character.add_experience(12345, 100)
        print(f'✅ 經驗值增加：')
        print(f'   - 當前等級：Lv.{result["level"]}')
        print(f'   - 當前經驗值：{result["experience"]}')
        print(f'   - 是否升級：{result["leveled_up"]}')
        print(f'   - 升級到的等級：{result["new_levels"]}')
    except Exception as e:
        print(f'❌ 升級失敗：{e}')
        return False

    print()

    # 6. 測試進度查詢
    print('6️⃣ 測試進度查詢...')
    try:
        progress = Character.get_progress(12345)
        print(f'✅ 進度信息：')
        print(f'   - 當前等級：Lv.{progress["level"]}')
        print(f'   - 當前經驗值：{progress["current_exp"]}')
        print(f'   - 升級所需經驗值：{progress["required_exp"]}')
        print(f'   - 進度：{progress["progress"]:.1f}%')
    except Exception as e:
        print(f'❌ 進度查詢失敗：{e}')
        return False

    print()

    # 7. 測試技能系統
    print('7️⃣ 測試技能系統（釣魚、挖礦）...')
    try:
        from database.skill import Skill
        
        Skill.add_experience(12345, 100, 'fishing')
        Skill.add_experience(12345, 50, 'mining')
        print('✅ 各技能經驗值添加成功')
        
        # 查詢玩家的所有技能
        player = Player.get_or_create_player(12345)
        print(f'\n   玩家 {player.display_name} 的所有技能：')
        for skill in player.skills:
            progress = Skill.get_progress(12345, skill.skill_type)
            print(f'   - {skill.skill_type}: Lv.{skill.level} (經驗：{skill.experience}/{progress["required_exp"]})')
    except Exception as e:
        print(f'❌ 技能系統測試失敗：{e}')
        return False

    print()
    print('✅ 所有測試通過！')
if __name__ == '__main__':
    success = test_level_system()
    exit(0 if success else 1)
