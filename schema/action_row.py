from dataclasses import dataclass

from schema.button import Button

@dataclass
class ActionRow:
    type: str = "action_row"
    components: list[Button] = None

    def __post_init__(self):
        if self.components and isinstance(self.components, list):
            for index, data in enumerate(self.components):
                if not isinstance(data, dict):
                    raise ValueError(f"components[{index}] 的資料必須為字典類型, 收到錯誤類型: {type(data)}")

                type_name = data.get("type")
                match type_name:
                    case "button":
                        self.components[index] = Button(**data)
                    case _:
                        raise ValueError(f"components[{index}] 收到不支援的元件類型: '{type_name}'")