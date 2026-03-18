import json
import os
from pathlib import Path

def convert_json_to_utf8(folder_path: str = "data/members"):
    """
    將 data/members 資料夾中所有 JSON 檔案轉換為 UTF-8 編碼
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"錯誤：資料夾不存在 - {folder_path}")
        return
    
    json_files = list(folder.glob("*.json"))
    
    if not json_files:
        print(f"警告：在 {folder_path} 中找不到 JSON 檔案")
        return
    
    converted_count = 0
    error_count = 0
    
    print(f"開始轉換 {len(json_files)} 個檔案...\n")
    
    for file_path in json_files:
        try:
            # 嘗試讀取檔案
            data = None
            encoding_used = None
            
            # 優先嘗試 utf-8
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    encoding_used = 'utf-8'
                    print(f"✓ {file_path.name} - 已是 UTF-8 編碼，無需轉換")
                    continue
            except UnicodeDecodeError:
                pass
            
            # 如果 utf-8 失敗，嘗試 cp950
            try:
                with open(file_path, 'r', encoding='cp950') as f:
                    data = json.load(f)
                    encoding_used = 'cp950'
            except UnicodeDecodeError:
                print(f"✗ {file_path.name} - 無法用 UTF-8 或 CP950 讀取，已跳過")
                error_count += 1
                continue
            except json.JSONDecodeError:
                print(f"✗ {file_path.name} - JSON 格式錯誤，已跳過")
                error_count += 1
                continue
            
            # 如果資料讀取成功，寫回 UTF-8
            if data is not None and encoding_used == 'cp950':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"✓ {file_path.name} - 從 CP950 轉換為 UTF-8 成功")
                converted_count += 1
        
        except Exception as e:
            print(f"✗ {file_path.name} - 發生錯誤：{e}")
            error_count += 1
    
    print(f"\n======== 轉換完成 ========")
    print(f"成功轉換：{converted_count} 個檔案")
    print(f"已是 UTF-8：{len(json_files) - converted_count - error_count} 個檔案")
    print(f"轉換失敗：{error_count} 個檔案")

if __name__ == "__main__":
    convert_json_to_utf8()
