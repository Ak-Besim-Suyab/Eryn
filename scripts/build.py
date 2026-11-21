from models import Building

updated = Building.update(level=1, experience=0.0).execute()
print(f"已重置 {updated} 筆 Building 資料（level=1, experience=0.0）。")
