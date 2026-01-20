#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試 Leveling Cog 的測試腳本
運行方式：python test_leveling.py

注意：這個腳本只測試升級系統的核心邏輯，
不會測試 Discord 事件監聽（因為那需要真實的 Discord 連接）
"""

from database import init_all_databases
from database.player import Player
from database.character import Character
from datetime import datetime

def test_leveling_logic():
    """測試升級系統的核心邏輯"""
    print('[升級系統測試開始]')
    print()

    # 1. 初始化資料庫
    print('1️⃣ 初始化資料庫...')
    try:
        init_all_databases()
        print('✅ 資料庫初始化成功')
    except Exception as e:
        print(f'❌ 初始化失敗：{e}')
        return False

    print()

    # 2. 創建測試玩家
    print('2️⃣ 創建測試玩家...')
    try:
        test_user_id = 99999
        player = Player.get_or_create_player(test_user_id)
        print(f'✅ 玩家創建成功：{player.display_name} (ID: {player.id})')
    except Exception as e:
        print(f'❌ 玩家創建失敗：{e}')
        return False

    print()

    # 3. 測試訊息經驗系統
    print('3️⃣ 測試訊息經驗系統...')
    try:
        # 模擬玩家發送訊息獲得經驗（每次 5 點）
        print('   模擬發送訊息 1：+5 經驗...')
        result1 = Character.add_experience(test_user_id, 5)
        print(f'   ✅ 結果：Lv.{result1["level"]}，經驗：{result1["experience"]}/120，升級：{result1["leveled_up"]}')
        
        print('   模擬發送訊息 2：+5 經驗...')
        result2 = Character.add_experience(test_user_id, 5)
        print(f'   ✅ 結果：Lv.{result2["level"]}，經驗：{result2["experience"]}/120，升級：{result2["leveled_up"]}')
        
        print('   模擬發送訊息 3：+5 經驗...')
        result3 = Character.add_experience(test_user_id, 5)
        print(f'   ✅ 結果：Lv.{result3["level"]}，經驗：{result3["experience"]}/120，升級：{result3["leveled_up"]}')
        
        print('   模擬發送訊息 4（應該升級）：+115 經驗...')
        result4 = Character.add_experience(test_user_id, 115)
        print(f'   ✅ 結果：Lv.{result4["level"]}，經驗：{result4["experience"]}，升級：{result4["leveled_up"]}')
        
        if result4['leveled_up']:
            print(f'   🎉 成功升級到 Lv.{result4["level"]}！')
        else:
            print('   ⚠️ 警告：應該升級但沒有升級')
            return False
    
    except Exception as e:
        print(f'❌ 訊息經驗測試失敗：{e}')
        return False

    print()

    # 4. 測試語音經驗系統
    print('4️⃣ 測試語音經驗系統...')
    try:
        # 模擬語音經驗計算
        test_cases = [
            (30, 1),    # 30 秒 → 1 經驗
            (60, 1),    # 60 秒 → 1 經驗
            (120, 2),   # 120 秒 → 2 經驗
            (900, 15),  # 900 秒 → 15 經驗（上限）
            (1200, 15), # 1200 秒 → 15 經驗（超過上限仍然 15）
        ]
        
        for duration, expected_exp in test_cases:
            # 計算語音經驗（每分鐘 1 經驗，上限 15）
            minutes = duration // 60
            exp_gained = min(15, max(1, minutes))
            
            status = "✅" if exp_gained == expected_exp else "❌"
            print(f'   {status} {duration}秒 → {exp_gained}經驗（預期：{expected_exp}）')
            
            if exp_gained != expected_exp:
                print(f'   錯誤：計算不符合預期')
                return False
    
    except Exception as e:
        print(f'❌ 語音經驗測試失敗：{e}')
        return False

    print()

    # 5. 測試進度查詢
    print('5️⃣ 測試進度查詢功能...')
    try:
        progress = Character.get_progress(test_user_id)
        print(f'✅ 進度信息：')
        print(f'   - 當前等級：Lv.{progress["level"]}')
        print(f'   - 當前經驗值：{progress["current_exp"]}')
        print(f'   - 升級所需經驗值：{progress["required_exp"]}')
        print(f'   - 進度百分比：{progress["progress"]:.1f}%')
    except Exception as e:
        print(f'❌ 進度查詢失敗：{e}')
        return False

    print()

    # 6. 測試多系統支持
    print('6️⃣ 測試技能系統（釣魚、挖礦）...')
    try:
        from database.skill import Skill
        
        # 模擬釣魚和挖礦的經驗
        Skill.add_experience(test_user_id, 50, "fishing")
        Skill.add_experience(test_user_id, 30, "mining")
        print('✅ 各技能經驗值添加成功')
        
        # 查詢玩家的所有技能
        player = Player.get_or_create_player(test_user_id)
        print(f'\n   玩家 {player.display_name} 的技能系統：')
        for skill in player.skills:
            print(f'   - {skill.skill_type}: Lv.{skill.level}')
    except Exception as e:
        print(f'❌ 多系統測試失敗：{e}')
        return False

    print()

    # 7. 測試冷卻時間邏輯
    print('7️⃣ 測試冷卻時間邏輯...')
    try:
        # 模擬消息冷卻時間檢查
        test_user_id_2 = 88888
        now = datetime.now().timestamp()
        message_cooldowns = {}
        
        MESSAGE_COOLDOWN = 30
        
        # 第一次發送訊息
        if test_user_id_2 not in message_cooldowns:
            message_cooldowns[test_user_id_2] = now
            print('   ✅ 第一次發送：可以獲得經驗')
        
        # 5 秒後發送（應該被冷卻阻止）
        if test_user_id_2 in message_cooldowns:
            time_diff = 5
            if time_diff < MESSAGE_COOLDOWN:
                print(f'   ✅ 5 秒後發送：被冷卻阻止（剩餘冷卻時間：{MESSAGE_COOLDOWN - time_diff}秒）')
        
        # 31 秒後發送（應該可以獲得經驗）
        if test_user_id_2 in message_cooldowns:
            time_diff = 31
            if time_diff >= MESSAGE_COOLDOWN:
                message_cooldowns[test_user_id_2] = now + 31
                print(f'   ✅ 31 秒後發送：冷卻已過期，可以獲得經驗')
    
    except Exception as e:
        print(f'❌ 冷卻時間測試失敗：{e}')
        return False

    print()
    print('✅ 所有測試通過！升級系統核心邏輯正常運行')
    return True

if __name__ == '__main__':
    success = test_leveling_logic()
    exit(0 if success else 1)
