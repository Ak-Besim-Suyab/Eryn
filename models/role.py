"""
"""

from dataclasses import dataclass
from cores.loader import JsonLoader
from cores.logger import logger

role_path = "assets/roles"


@dataclass
class Role:
    id: str
    name: str
    icon: str
    category: str
    tag: str

class RoleManager:
    def __init__(self):
        self._roles: dict[str, Role] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(role_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"RoleManager | 找不到資料夾: {role_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"RoleManager | {filename} 的 JSON 格式錯誤")
                continue
            
            try:
                role = Role(**data)
                self._roles[role.id] = role
                total_files += 1
                logger.info(f"RoleManager | 載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"RoleManager | {filename} 的 JSON 格式與 Role 類別不相容: {e}")
                continue
        
        logger.info(f"RoleManager | 資料載入完畢，總共載入 {total_files} 個檔案")

    def get_role(self, role_id: str) -> Role | None:
        return self._roles.get(role_id)

    def get_role_by_category(self, category: str) -> list[Role]:
        record = []
        for _, role in self._roles.items():
            if role.category == category:
                record.append(role)
        return record

    def get_role_by_tag(self, tag: str) -> list[Role]:
        record = []
        for _, role in self._roles.items():
            if role.tag == tag:
                record.append(role)
        return record

    def get_all_roles(self) -> list[Role]:
        return list(self._roles.values())

# 建立唯一實例
role_manager = RoleManager()
