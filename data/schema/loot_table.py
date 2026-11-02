import random
from collections import Counter
from dataclasses import dataclass, field

@dataclass
class Entry:
    type: str
    id: str
    weight: int
    min: int
    max: int

@dataclass
class LootTable:
    id: str
    entries: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.entries = [Entry(**entry) if isinstance(entry, dict) else entry for entry in self.entries]

    def roll(self, times: int = 1) -> Counter:
        """
        抽取戰利品表, 返回一個 Counter 物件, key 為 tuple[item_type, item_id], value 為 quantity
        """
        rewards = Counter()
        for _ in range(times):
            entry = random.choices(self.entries, weights = [entry.weight for entry in self.entries])[0]
            rewards[(entry.type, entry.id)] += random.randint(entry.min, entry.max)

        return rewards