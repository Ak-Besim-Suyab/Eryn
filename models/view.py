from dataclasses import dataclass, field

from .select import Select
from .button import Button

@dataclass
class View:
    timeout: float | None = 300

    selects: list[Select] = field(default_factory = list)
    buttons: list[Button] = field(default_factory = list)

    def __post_init__(self):
        if self.selects and isinstance(self.selects, list) and isinstance(self.selects[0], dict):
            self.selects = [Select(**s) for s in self.selects]

        if self.buttons and isinstance(self.buttons, list) and isinstance(self.buttons[0], dict):
            self.buttons = [Button(**b) for b in self.buttons]
