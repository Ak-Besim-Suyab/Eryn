"""
這個物件用於讀取整個目標資料夾下的所有 json, yaml 檔案
調用方法後會回傳 resources 字典, key 為檔案名, value 為檔案內容

移除對資料的型別檢查, 直接將檔案內容以 dict 或 list 的形式回傳, 由註冊器處理資料結構
"""

import json
import yaml
from pathlib import Path

from cores.logger import logger

filename_extension = {".json", ".yaml", ".yml"}

def load(path: str) -> dict[str, dict | list]:

    folder = Path(path)
    if not folder.exists(): 
        raise FileNotFoundError(f"錯誤，找不到資料夾: {path}")

    data = {}
    data_total = 0
    
    for file in folder.rglob("*"):
        if file.suffix.lower() not in filename_extension:
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

                # if not isinstance(d, dict): 
                #     logger.exception(f"檔案格式不為字典, 已略過: {file.name}")
                #     continue

                if file.stem in d: 
                    logger.debug(f"檔名重複, 已略過: {file.name}")
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