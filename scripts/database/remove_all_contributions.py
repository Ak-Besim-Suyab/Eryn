"""
移除整個 Contribution table 的資料
"""
from models import Contribution

deleted = Contribution.delete().execute()

print(f"已刪除 {deleted} 筆 Contribution 資料")