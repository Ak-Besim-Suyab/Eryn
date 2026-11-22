from dataclasses import dataclass

@dataclass
class Material:
    id: str
    name: str
    icon: str = "📦"
