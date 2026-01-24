from context import Context
from utils.logger import logger


class LootTableManager:
    def __init__(self):
        self._registry = {}

    def register(self, name: str, source):
        if name in self._registry:
            raise ValueError(
                f"LootTable '{name}' 已被註冊，避免重複註冊同一個名稱"
            )

        loot_table = None
        if isinstance(source, str):
            loot_table = Context.json_loader.load(source)
            if not loot_table:
                logger.error(f"[LootTable] 載入失敗：{source}")
                return
            logger.info(f"[LootTable] 已註冊 {name}，來源 {source}")
        else:
            loot_table = source
            logger.info(f"[LootTable] 已註冊 {name}（物件註冊）")

        self._registry[name] = loot_table

    def get(self, name: str):
        return self._registry.get(name)

    def exists(self, name: str) -> bool:
        return name in self._registry

    def list_tables(self) -> list[str]:
        return list(self._registry.keys())