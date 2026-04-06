"""
這是個簡單的遷移腳本，用於修改特定的欄位名稱與值
"""
from playhouse.migrate import *
from configuration import db
from models.player import Player

# 這裡假設你底層使用的是 SQLite
migrator = SqliteMigrator(db)

def run():

    print("開始執行資料庫遷移...")
    
    try:
        # 這個方法會將指定 table 的欄位名稱 old_name 修改為新的欄位名稱 new_name
        # 例：現在將為 player 資料表中的欄位名稱 location 重新命名為欄位名稱 region
        migrate(migrator.rename_column('player', 'location', 'region'))
        print("✅ 欄位重新命名成功！")
    except Exception as e:
        print(f"⚠️ 重新命名失敗 (可能已經改過了或欄位不存在): {e}")

    # 這裡則會調用 model, 並將欄位內的值更新為新的值
    # 例：這裡將所有玩家的 region 重置為初始值 "falun"
    # 這等同於 SQL 的 UPDATE player SET region = 'falun';
    query = Player.update(region="falun")
    updated_count = query.execute()
    
    print(f"✅ 成功重置了 {updated_count} 位玩家的區域位置！")

if __name__ == "__main__":
    run()