from dataclasses import dataclass

@dataclass
class Button:
    custom_id: str | None = None
    label: str | None = None
    emoji: str | None = None
    callback: str | None = None
    style: str = "primary"