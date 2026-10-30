from dataclasses import dataclass

@dataclass
class Resource:
    id: str
    name: str
    emoji: str = "📦"