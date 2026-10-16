from discord import ui, SeparatorSpacing

def build_text(data: str) -> ui.TextDisplay:
    return ui.TextDisplay(content = data['content'])

def build_seperator(size: str = "large", visible: bool = True) -> ui.Separator:
    spacing = SeparatorSpacing.large if size == "large" else SeparatorSpacing.small
    return ui.Separator(spacing = spacing, visible = visible)

builders = {
    "text": build_text,
    "separator": build_seperator
}

def build_container(data: dict) -> ui.Container:
    container = ui.Container()
    container.accent_color = data.get("accent_color")

    for index, item_data in enumerate(data["items"]):
        type_name = item_data["type"]
        builder = builders[type_name]
        if builder is None:
            raise ValueError(f"items[{index}] 有未知的元件類型: {type_name}")

        try:
            container.add_item(builder(item_data))
        except KeyError as e:
            raise ValueError(f"items[{index}] ({type_name}) 缺少必要的屬性: {e}")
        
    return container