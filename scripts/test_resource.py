from lib import resource

""" 對資源函式單元測試
    這裡標記假成員資料並測試驗證是否正常運作
"""

# 測試所有參數是否正常, 並印出所有參數值
obj = resource.give(1, "wood", 5)
if obj:
    print(f"wood={obj.wood}, stone={obj.stone}, food={obj.food}")

# 測試數量驗證
obj = resource.give(1, "wood", -5)
# 測試名稱驗證
obj = resource.give(1, "somthing", 5)