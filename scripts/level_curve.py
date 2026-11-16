"""
這個腳本用於測試與查看等級曲線, 需要記錄過程所以不要刪除
"""

def get_req_exp(level: int):
    base = 1350
    exponent = 1.15

    return round((base * level ** exponent) / 10) * 10

for i in range(1, 50):
    print(i, get_req_exp(i), get_req_exp(i) - get_req_exp(i - 1))