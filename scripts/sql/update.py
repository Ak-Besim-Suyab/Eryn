"""
更新資料腳本, 這個腳本用於批次更新資料庫的資料, 更新單個欄位時不需要加上 where 查詢條件
"""
from model import Player

updated = Player.update(region="haven").execute()

print(f"已更新 {updated} 筆")