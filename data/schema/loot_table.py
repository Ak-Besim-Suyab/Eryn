import random
from collections import Counter
from dataclasses import dataclass, field

@dataclass
class Entry:
    type: str
    id: str
    weight: int
    count: int

@dataclass
class LootTable:
    pools: list[Entry] = field(default_factory=list)

    def __post_init__(self):
        self.pools = [Entry(**entry) if isinstance(entry, dict) else entry for entry in self.pools]

    def roll(self, times: int = 1) -> Counter:
        """
        抽取戰利品表，將所有抽取結果存入 Counter 物件並返回，key 為 tuple[item_type, item_id]，value 為 quantity
        """
        if not self.pools:
            return Counter()

        weights = [entry.weight for entry in self.pools]
        rewards = Counter()
        for _ in range(times):
            entry = random.choices(self.pools, weights=weights)[0]
            rewards[(entry.type, entry.id)] += random.randint(1, entry.count)

        return rewards