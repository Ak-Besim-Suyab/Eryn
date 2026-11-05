from dataclasses import dataclass, field

@dataclass
class Race:
    id: str
    name: str
    equip_slots: list = field(default_factory=list)