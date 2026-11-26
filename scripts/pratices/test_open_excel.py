"""
導入 excel 的設定暫時被棄用，維持 yaml 格式
"""

from lib.util import file

# 獲取 Excel 檔案 (work book)
wb = file.load_excel("data/building.xlsx")

# 獲取指定名稱的工作表 (work sheet)

data: dict[str, dict] = {}
for name in wb.sheetnames:
    ws = wb[name]
    header, *body = ws.iter_rows(values_only=True)

    requirements = []
    for row in body:
        requirements.append(dict(zip(header, row)))

    data[name] = {"requirements": requirements}

dc = {}
for n, d in data.items():
    pass

print(dc)

building = dc.get("modelhouse")
print(building.requirements[0].level)

# ws = wb["sanctuary"]

# 這裡是將第一行 (row) 作為標頭 (level, wood, stone.. etc.), 其他行則會成為 body (tuple)
# 要記得 values_only=True 不然會返回 openpyxl 的 Cell 物件
# header, *body = ws.iter_rows(values_only=True)

# 建立一個空串列用來接住將標投與值以 zip() 函式合併並轉為字典的結果
# record = []
# for row in body:
#     record.append(dict(zip(header, row)))

# 印出結果查看是否符合需求結構
# print(record)

# 嘗試查詢資料是否包含自己需要的結果
# level = 3
# if any(r.get("level") == level for r in record):
#     print("有等級為 3 的建築")
# else:
#     print("建築已滿等")

# 將資源名稱提出
# level, *resources = header

# 理論上要返回 level 與 wood, stone, food.. etc. string 結果
# print(level, resources)