"""
本函式庫用於讀取目標 directory 所有 json, yaml, yml 檔案, 讀取後會回傳 dict, key 為檔案名, value 為檔案內容
"""

import json
import yaml
from pathlib import Path
from cores.logger import logger

filenames = {".json", ".yaml", ".yml"}

def load_dir(path: str) -> dict[str, dict]:

    folder = Path(path)
    if not folder.exists(): 
        raise FileNotFoundError(f"錯誤，找不到資料夾: {path}")

    data = {}
    data_total = 0 # 統計成功載入的檔案數量
    
    for file in folder.rglob("*"):
        if file.suffix.lower() not in filenames:
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                match file.suffix:
                    case ".json":
                        d = json.load(f)
                    case ".yaml" | ".yml":
                        d = yaml.safe_load(f)

                if not d: 
                    logger.debug(f"檔案內容為空, 已略過: {file.name}")
                    continue
                if file.stem in d: 
                    logger.debug(f"檔案名稱重複, 已略過: {file.name}")
                    continue
                
                data[file.stem] = d
                data_total += 1
                logger.info(f"載入檔案成功: {file.name}")

        except json.JSONDecodeError as e: 
            logger.exception(f"json 格式錯誤: {file.name}: {e}")
            continue
        except yaml.YAMLError as e: 
            logger.exception(f"yaml 格式錯誤: {file.name}: {e}")
            continue
        except Exception as e: 
            logger.exception(f"錯誤，無法讀取 {file.name}: {e}")
            continue
    
    logger.info(f"資料載入完畢，總共載入 {data_total} 個檔案")
    return data