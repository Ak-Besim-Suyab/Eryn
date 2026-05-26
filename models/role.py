from dataclasses import dataclass

@dataclass
class Role:
    id: str
    discord_id: int
    name: str
    icon: str
    category: str
    tag: str
