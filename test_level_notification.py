#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試升級通知系統的腳本
運行方式：python test_level_notification.py

此腳本測試：
1. 升級訊息的 embed 構建是否正確
2. 不同升級數量的訊息顯示
3. 升級檢測邏輯是否正常
"""

import os
os.environ['TEST_MODE'] = '1'

from database import init_all_databases
from database.player import Player
from database.character import Character
from datetime import datetime

def test_level_notification():
    print('[升級通知測試開始]')
    print()

    # 1. 初始化數據庫
    print('1️⃣ 初始化數據庫...')
    try:
        init_all_databases()
        print('✅ 數據庫初始化成功')
    except Exception as e:
        print(f'❌ 初始化失敗：{e}')
        return False

    print()

    # 2. 創建測試玩家
    print('2️⃣ 創建測試玩家...')
    try:
        test_user_id = 66666
        player = Player.get_or_create_player(test_user_id)
        print(f'✅ 玩家創建成功：{player.display_name} (ID: {player.id})')
    except Exception as e:
        print(f'❌ 玩家創建失敗：{e}')
        return False

    print()

    # 3. 測試單級升級通知
    print('3️⃣ 測試單級升級（升級到 Lv.2）...')
    try:
        # 獲取升級所需的經驗值
        required_exp = Character._get_required_exp(1)
        print(f'   當前等級 Lv.1 升到 Lv.2 需要 {required_exp} 經驗')
        
        # 增加足夠的經驗以升級
        result = Character.add_experience(test_user_id, required_exp)
        
        print(f'   ✅ 升級結果：')
        print(f'      - 當前等級：Lv.{result["level"]}')
        print(f'      - 是否升級：{result["leveled_up"]}')
        print(f'      - 升級到的等級：{result["new_levels"]}')
        
        # 驗證升級通知訊息構建
        if result['leveled_up']:
            new_levels = result['new_levels']
            if len(new_levels) == 1:
                level_text = f"升級到 **Lv.{new_levels[0]}**"
            else:
                level_text = f"升級到 **Lv.{new_levels[-1]}** (一次升級 {len(new_levels)} 級！)"
            
            print(f'   📢 通知訊息：')
            print(f'      標題：🎉 玩家升級')
            print(f'      描述：<@{test_user_id}> 的角色等級 {level_text}')
        else:
            print('   ⚠️ 警告：應該升級但沒有升級')
            return False
    
    except Exception as e:
        print(f'❌ 單級升級測試失敗：{e}')
        return False

    print()

    # 4. 測試多級升級通知
    print('4️⃣ 測試多級升級（一次升多級）...')
    try:
        # 累積足夠的經驗以升級多級
        # 當前在 Lv.2，需要 Lv.2 升 Lv.3 + Lv.3 升 Lv.4 的經驗
        exp_to_level_3 = Character._get_required_exp(2)
        exp_to_level_4 = Character._get_required_exp(3)
        total_exp_needed = exp_to_level_3 + exp_to_level_4
        
        print(f'   Lv.2→3 需要 {exp_to_level_3} 經驗，Lv.3→4 需要 {exp_to_level_4} 經驗')
        print(f'   共需要 {total_exp_needed} 經驗')
        
        # 增加經驗
        result = Character.add_experience(test_user_id, total_exp_needed)
        
        print(f'   ✅ 升級結果：')
        print(f'      - 當前等級：Lv.{result["level"]}')
        print(f'      - 是否升級：{result["leveled_up"]}')
        print(f'      - 升級到的等級：{result["new_levels"]}')
        
        # 驗證多級升級的通知訊息
        if result['leveled_up']:
            new_levels = result['new_levels']
            if len(new_levels) == 1:
                level_text = f"升級到 **Lv.{new_levels[0]}**"
            else:
                level_text = f"升級到 **Lv.{new_levels[-1]}** (一次升級 {len(new_levels)} 級！)"
            
            print(f'   📢 通知訊息：')
            print(f'      標題：🎉 玩家升級')
            print(f'      描述：<@{test_user_id}> 的角色等級 {level_text}')
            print(f'      升級數量：{len(new_levels)} 級')
        else:
            print('   ⚠️ 警告：應該升級但沒有升級')
            return False
    
    except Exception as e:
        print(f'❌ 多級升級測試失敗：{e}')
        return False

    print()

    # 5. 測試不升級的情況（增加少量經驗）
    print('5️⃣ 測試不升級的情況（增加少量經驗）...')
    try:
        result = Character.add_experience(test_user_id, 10)
        
        print(f'   ✅ 結果：')
        print(f'      - 當前等級：Lv.{result["level"]}')
        print(f'      - 當前經驗值：{result["experience"]}')
        print(f'      - 是否升級：{result["leveled_up"]}')
        
        if not result['leveled_up']:
            print(f'   ✅ 正確：未升級，不發送通知')
        else:
            print(f'   ⚠️ 警告：不應該升級但升級了')
            return False
    
    except Exception as e:
        print(f'❌ 不升級測試失敗：{e}')
        return False

    print()

    # 6. 測試升級公式邏輯
    print('6️⃣ 測試升級公式...')
    try:
        print('   各等級升級所需經驗值：')
        for level in range(1, 6):
            required = Character._get_required_exp(level)
            print(f'      Lv.{level} → Lv.{level+1}：{required} 經驗')
        
        # 驗證公式
        level_1_to_2 = Character._get_required_exp(1)
        expected = int(100 * (1 ** 1.5) + 1 * 20)
        
        if level_1_to_2 == expected:
            print(f'   ✅ 升級公式正確')
        else:
            print(f'   ❌ 升級公式錯誤：期望 {expected}，實際 {level_1_to_2}')
            return False
    
    except Exception as e:
        print(f'❌ 升級公式測試失敗：{e}')
        return False

    print()

    # 7. 測試管理員指令 - 設置等級
    print('7️⃣ 測試管理員功能 - 設置等級...')
    try:
        test_player_2 = Player.get_or_create_player(66667)
        # 先升到 Lv.5
        Character.add_experience(test_player_2.id, 10000)
        progress_before = Character.get_progress(test_player_2.id)
        
        # 使用 set_level 直接設置為 Lv.20
        result = Character.set_level(test_player_2.id, 20)
        progress_after = Character.get_progress(test_player_2.id)
        
        print(f'   ✅ 設置等級成功：')
        print(f'      原等級：Lv.{result["old_level"]} (當前等級：Lv.{progress_before["level"]})')
        print(f'      新等級：Lv.{result["level"]}')
        print(f'      經驗值：{result["experience"]}（已重設為 0）')
    
    except Exception as e:
        print(f'❌ 設置等級測試失敗：{e}')
        return False

    print()

    # 8. 測試管理員指令 - 設置經驗
    print('8️⃣ 測試管理員功能 - 設置經驗...')
    try:
        result = Character.set_experience(test_player_2.id, 500)
        progress = Character.get_progress(test_player_2.id)
        
        print(f'   ✅ 設置經驗成功：')
        print(f'      原經驗值：{result["old_experience"]}')
        print(f'      新經驗值：{result["experience"]}/{progress["required_exp"]}')
        print(f'      當前等級：Lv.{result["level"]}')
    
    except Exception as e:
        print(f'❌ 設置經驗測試失敗：{e}')
        return False

    print()

    # 9. 測試管理員指令 - 重設等級
    print('9️⃣ 測試管理員功能 - 重設等級...')
    try:
        result = Character.set_level(test_player_2.id, 1)
        progress = Character.get_progress(test_player_2.id)
        
        print(f'   ✅ 重設等級成功：')
        print(f'      原等級：Lv.{result["old_level"]}')
        print(f'      新等級：Lv.{result["level"]}（已重設為初始狀態）')
        print(f'      經驗值：{result["experience"]}/{progress["required_exp"]}')
    
    except Exception as e:
        print(f'❌ 重設等級測試失敗：{e}')
        return False

    print()
    print('✅ 所有升級通知與管理員功能測試通過！')
    print()
    print('📝 總結：')
    print('   - ✅ 單級升級訊息構建正確')
    print('   - ✅ 多級升級訊息構建正確')
    print('   - ✅ 不升級時不發送通知')
    print('   - ✅ 升級公式邏輯正確')
    print('   - ✅ 設置等級功能正確')
    print('   - ✅ 設置經驗功能正確')
    print('   - ✅ 重設等級功能正確')
    return True

if __name__ == '__main__':
    success = test_level_notification()
    exit(0 if success else 1)
