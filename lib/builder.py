import discord
from discord import ui, SeparatorSpacing

from schema.container import Text, Separator, Section
from schema import Container, ActionRow, Select

def text(item: Text) -> ui.TextDisplay:
    return ui.TextDisplay(content = item.content)

def seperator(item: Separator) -> ui.Separator:
    spacing = SeparatorSpacing.small if item.size == "small" else SeparatorSpacing.large
    return ui.Separator(spacing = spacing, visible = item.visible)

def section(item: Section) -> ui.Section:
    match item.accessory.type:
        case "button":
            accessory = ui.Button(label = item.accessory.label, url = item.accessory.url, emoji = item.accessory.emoji)
        case "thumbnail":
            accessory = ui.Thumbnail(media = item.accessory.media)
    return ui.Section(item.content, accessory = accessory)

def action_row(item: ActionRow) -> ui.ActionRow:

    row = ui.ActionRow()

    for component in item.components:
        match component.type:
            case "button":
                row.add_item(ui.Button(label = component.label, url = component.url, emoji = component.emoji))

    return row

def select(item: Select) -> ui.ActionRow:

    row = ui.ActionRow()

    options = []

    for option in item.options:
        o = discord.SelectOption(
            label = option.label,
            emoji = option.emoji,
            description = option.description,
            value = option.value
        )
        options.append(o)

    select = ui.Select(
        placeholder = item.placeholder,
        min_values = item.min_values,
        max_values = item.max_values,
        custom_id = item.custom_id,
        options = options
    )
    row.add_item(select)

    return row

builders = {
    "text": text,
    "separator": seperator,
    "section": section,
    "action_row": action_row,
    "select": select,
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