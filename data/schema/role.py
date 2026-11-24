from dataclasses import dataclass

@dataclass
class Role:
    id: int
    display_name: str
    emoji: str
    category: str
    tag: str