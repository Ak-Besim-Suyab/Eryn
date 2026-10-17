from dataclasses import dataclass, field

from schema.button import Button
from schema.action_row import ActionRow

@dataclass
class Text:
    type: str = "text"
    content: str = ""

@dataclass
class Separator:
    type: str = "separator"
    size: str = "large"
    visible: bool = True

@dataclass
class Thumbnail:
    type: str = "thumbnail"
    media: str = ""

@dataclass
class Section:
    type: str = "section"
    content: str = ""
    accessory: Button | Thumbnail | dict = None

    def __post_init__(self):
        if self.accessory and isinstance(self.accessory, dict):
            type_name = self.accessory.get("type")
            match type_name:
                case "button":
                    self.accessory = Button(**self.accessory)
                case "thumbnail":
                    self.accessory = Thumbnail(**self.accessory)
                case _:
                    raise ValueError(f"accessory 的資料格式必須為 button 或 thumbnail, 收到錯誤類型: {type_name}")

@dataclass
class Container:
    accent_color: int = 0
    items: list = field(default_factory=list)

    def __post_init__(self):
        """
        將 items 中的字典資料轉換為對應的物件實例
        """
        if self.items and isinstance(self.items, list):
            for index, item in enumerate(self.items):
                if not isinstance(item, dict):
                    raise ValueError(f"items[{index}] 的資料必須為字典類型, 收到錯誤類型: {type(item)}")

                type_name = item.get("type")
                match type_name:
                    case "text":
                        self.items[index] = Text(**item)
                    case "separator":
                        self.items[index] = Separator(**item)
                    case "section":
                        self.items[index] = Section(**item)
                    case "action_row":
                        self.items[index] = ActionRow(**item)
                    case _:
                        raise ValueError(f"items[{index}] 收到不支援的元件類型: '{type_name}'")