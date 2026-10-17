from discord import ui, SeparatorSpacing

from schema.container import Container, Text, Separator

def text(item: Text) -> ui.TextDisplay:
    return ui.TextDisplay(content = item.content)

def seperator(item: Separator) -> ui.Separator:
    spacing = SeparatorSpacing.small if item.size == "small" else SeparatorSpacing.large
    return ui.Separator(spacing = spacing, visible = item.visible)

builders = {
    "text": text,
    "separator": seperator
}

def build_container(data: Container) -> ui.Container:
    container = ui.Container()
    container.accent_color = data.accent_color

    for index, item_object in enumerate(data.items):

        type_name = item_object.type

        builder = builders.get(type_name)
        if builder is None:
            raise ValueError(f"items[{index}] 有未知的元件類型: {type_name}")

        try:
            container.add_item(builder(item_object))
        except KeyError as e:
            raise ValueError(f"items[{index}] ({type_name}) 缺少必要的屬性: {e}")
        
    return container