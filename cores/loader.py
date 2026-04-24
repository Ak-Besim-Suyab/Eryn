"""
這個物件用於讀取整個目標資料夾下的所有 json, yaml 檔案
調用方法後會回傳 resources 字典, key 為檔案名, value 為檔案內容
"""

import json
import yaml
from pathlib import Path
from typing import TypeVar, Type

from cores.logger import logger

T = TypeVar('T')

class AssetLoader:
    @staticmethod
    def load(path: str | Path, model: Type[T]) -> dict[str, T]:
        
        # 檢查資料夾是否存在
        folder = Path(path)
        if not folder.exists():
            raise FileNotFoundError(f"錯誤，找不到資料夾: {path}")
        
        filename_extension = {".json", ".yaml", ".yml"}

        resources: dict[str, T] = {}

        total_file = 0
        for file in folder.rglob("*"):

            if file.suffix.lower() not in filename_extension:
                continue

            try:
                with open(file, "r", encoding="utf-8") as f:

                    match file.suffix:
                        case ".json":
                            data = json.load(f)
                        case ".yaml" | ".yml":
                            data = yaml.safe_load(f)

                    if data is None:
                        logger.debug(f"檔案內容為空: {file.name}, 已跳過, 請確認是否為允許的檔案內容.")
                        continue

                    if not isinstance(data, dict):
                        logger.exception(f"檔案內容格式錯誤: {file.name}, 已跳過, 請確認是否為允許的檔案內容.")
                        continue

                    try:
                        obj = model(**data)
                    except TypeError as e:
                        logger.exception(f"{file.name} 的 JSON 格式與 {model.__name__} 類別不相容: {e}")
                        continue
                    
                    # 如果資料有 id 欄位, 使用 id 欄位作為 key, 若沒有則以檔案名稱作為字典的 key
                    key = getattr(obj, "id", file.stem)

                    if key in resources:
                        logger.debug(f"發現重複的檔名: {file.name}, 已跳過, 請確認檔案名稱是否重複.")
                        continue

                    resources[key] = obj

                    total_file += 1
                    logger.info(f"載入檔案成功: {file.name}")

            except json.JSONDecodeError as e:
                logger.exception(f"json 格式錯誤: {file.name}, 原因: {e}")
                continue

            except yaml.YAMLError as e:
                logger.exception(f"yaml 格式錯誤: {file.name}, 原因: {e}")
                continue
            
            except Exception as e:
                logger.exception(f"錯誤，無法讀取 {file.name}, 出現未預期的錯誤")
                continue
        
        logger.info(f"資料載入完畢，總共載入 {total_file} 個檔案")
        return resources