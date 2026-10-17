from dataclasses import dataclass, field

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
                    case _:
                        raise ValueError(f"items[{index}] 收到不支援的元件類型: '{type_name}'")