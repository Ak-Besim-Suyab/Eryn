import discord
from discord import ui, SeparatorSpacing

from data.schema import Text, Separator, Section, Container, ActionRow, Select

from lib.utils import SafeDict

BUTTON_STYLE = {
    "primary"   : discord.ButtonStyle.primary,
    "secondary" : discord.ButtonStyle.secondary,
    "danger"    : discord.ButtonStyle.danger,
    "link"      : discord.ButtonStyle.link,
}

# 建構生產器元件
def text(item: Text, **kwargs) -> ui.TextDisplay:
    return ui.TextDisplay(content = item.content.format_map(SafeDict(kwargs)))

def seperator(item: Separator, **kwargs) -> ui.Separator:
    spacing = SeparatorSpacing.small if item.size == "small" else SeparatorSpacing.large
    return ui.Separator(spacing = spacing, visible = item.visible)

def section(item: Section, **kwargs) -> ui.Section:

    match item.accessory.type:
        case "button":
            accessory = ui.Button(label=item.accessory.label, url=item.accessory.url, emoji=item.accessory.emoji)
        case "thumbnail":
            accessory = ui.Thumbnail(media=item.accessory.media.format_map(SafeDict(kwargs)))

    return ui.Section(item.content.format_map(SafeDict(kwargs)), accessory = accessory)

def action_row(item: ActionRow, **kwargs) -> ui.ActionRow:

    row = ui.ActionRow()
    for component in item.components:
        match component.type:
            case "button":
                row.add_item(
                    ui.Button(
                        style=BUTTON_STYLE.get(component.style, discord.ButtonStyle.secondary), 
                        label=component.label, 
                        url=component.url, 
                        emoji=component.emoji,
                        custom_id=component.custom_id
                    )
                )

    return row

def select(item: Select, **kwargs) -> ui.ActionRow:

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

# 建構生產器元件字典
builders = {
    "text": text,
    "separator": seperator,
    "section": section,
    "action_row": action_row,
    "select": select,
}

# 建構生產器
def build_container(data: Container, **kwargs) -> ui.Container:
    container = ui.Container()
    container.accent_color = data.accent_color

    for index, item_object in enumerate(data.items):

        type_name = item_object.type

        builder = builders.get(type_name)
        if builder is None:
            raise ValueError(f"items[{index}] 有未知的元件類型: {type_name}")

        try:
            container.add_item(builder(item_object, **kwargs))
        except KeyError as e:
            raise ValueError(f"items[{index}] ({type_name}) 缺少必要的屬性: {e}")
        
    return container