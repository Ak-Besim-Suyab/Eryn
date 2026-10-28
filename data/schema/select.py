from dataclasses import dataclass, field

@dataclass
class Select:
    type: str = "select"
    placeholder: str | None= None
    min_values: int = 1
    max_values: int = 1
    custom_id: str | None = None
    callback: str | None = None
    options: list[SelectOption] = field(default_factory=list)

    def __post_init__(self):
        if self.options and isinstance(self.options, list) and isinstance(self.options[0], dict):
            self.options = [SelectOption(**o) for o in self.options]

@dataclass
class SelectOption:
    label: str = None
    description: str = None
    emoji: str = None
    value: str = None