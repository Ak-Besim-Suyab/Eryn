from dataclasses import dataclass, field

@dataclass
class SelectOption:
    label: str = None
    value: str = None
    description: str = None
    emoji: str = None

@dataclass
class Select:
    """
    .. note::
        大部分情況，選項清單應該都會交由 Query 請求, 僅使用 `custom_id` 作為參數, `options` 則留空
        但保留特別情況下會提供特殊選項, 因此仍需設計 `options` 參數, 以便以資料結構的形式直接傳入選項資料
    """
    custom_id: str | None = None
    placeholder: str | None= None
    min_values: int = 1
    max_values: int = 1
    callback: str | None = None
    options: list[SelectOption] = field(default_factory=list)

    def __post_init__(self):
        if self.options and isinstance(self.options, list) and isinstance(self.options[0], dict):
            self.options = [SelectOption(**o) for o in self.options]