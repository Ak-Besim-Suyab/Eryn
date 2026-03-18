"""
這個物件用來存放身分組資料
導入時請導入唯一實例
"""
import json

from pathlib import Path
from cores.logger import logger

ROLE_PATH = "data/roles/"

class RoleManager:
    def __init__(self):
        self._roles = {}
        self._load()

    def _load(self):
        folder = Path(ROLE_PATH)

        if not folder.exists():
            raise FileNotFoundError(f"RoleManager | 找不到資料夾: {ROLE_PATH}")
        
        total_files = 0
        total_roles = 0

        for file in folder.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    for role in data:
                        role_id = role.get("role_id")
                        if role_id:
                            self._roles[role_id] = role

                count = len(data)
                total_files += 1
                total_roles += count
                logger.info(f"RoleManager | 載入 {file.name} 成功，總共載入 {count} 個身分組")

            except Exception as e:
                logger.error(f"RoleManager | 無法讀取 {file.name}: {e}")

            except json.JSONDecodeError:
                logger.error(f"RoleManager | {file.name} 的 JSON 格式錯誤: {e}")

        logger.info(f"RoleManager | 資料載入完畢，總共載入 {total_files} 個檔案，包含 {total_roles} 個身分組")

    def get_role(self, role_id: int):
        role = self._roles.get(role_id)
        if not role:
            raise KeyError(f"RoleManager | 發生錯誤，找不到 {role_id} 身分組資料，請確認名稱是否正確，或檔案是否遺失。")
        return self._roles[role_id]

role_manager = RoleManager()