from dataclasses import dataclass

@dataclass
class Button:
    type: str = "button"
    style: str = "primary"
    label: str | None = None
    emoji: str | None = None
    url: str | None = None
    custom_id: str | None = None
    callback: str = "on_interaction"