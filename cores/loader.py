import json
from pathlib import Path
from cores.logger import logger

class JsonLoader:
    """
    這個物件用於讀取整個目標資料夾下的所有 json 檔案
    調用方法後會回傳 resources 字典, key 為檔案名, value 為檔案內容
    """
    @staticmethod
    def load(folder_path: str | Path) -> dict[str, dict]:
        resources = {}
        folder = Path(folder_path)

        # 檢查資料夾是否存在
        if not folder.exists():
            raise FileNotFoundError(f"錯誤，找不到資料夾: {folder_path}")
        
        # 開始讀取目標資料夾下的所有 json 檔案
        for file in folder.rglob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    resource = json.load(f)
                    resources[file.stem] = resource

            except json.JSONDecodeError:
                logger.error(f"錯誤，檔案格式錯誤: {file.name}")
                continue
            
            except Exception as e:
                logger.error(f"錯誤，無法讀取 {file.name}, 原因: {e}")
                continue
        
        return resources