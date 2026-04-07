import json
import yaml
from pathlib import Path
from cores.logger import logger

class AssetLoader:
    """
    這個物件用於讀取整個目標資料夾下的所有 json, yaml 檔案
    調用方法後會回傳 resources 字典, key 為檔案名, value 為檔案內容
    """
    @staticmethod
    def load(folder_path: str | Path) -> dict[str, dict]:
        
        # 檢查資料夾是否存在
        folder = Path(folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"錯誤，找不到資料夾: {folder_path}")
        
        filename_extension = {".json", ".yaml", ".yml"}
        
        # 開始讀取目標資料夾下的所有 json 檔案
        resources = {}
        for file in folder.rglob("*"):

            if file.suffix.lower() not in filename_extension:
                continue

            try:
                with open(file, "r", encoding="utf-8") as f:

                    match file.suffix:
                        case ".json":
                            resource = json.load(f)
                        case ".yaml" | ".yml":
                            resource = yaml.safe_load(f)

                    if resource is None:
                        logger.debug(f"檔案內容為空: {file.name}, 已跳過, 請確認是否為允許的檔案內容.")
                        continue

                    if file.stem in resources:
                        logger.debug(f"發現重複的檔名: {file.name}, 已跳過, 請確認檔案名稱是否重複.")
                        continue

                    resources[file.stem] = resource

            except json.JSONDecodeError as e:
                logger.error(f"json 格式錯誤: {file.name}, 原因: {e}")
                continue

            except yaml.YAMLError as e:
                logger.error(f"yaml 格式錯誤: {file.name}, 原因: {e}")
                continue
            
            except Exception as e:
                logger.error(f"錯誤，無法讀取 {file.name}, 原因: {e}")
                continue
        
        return resources