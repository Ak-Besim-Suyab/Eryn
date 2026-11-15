import discord
from discord import ui

from data import schema

from lib.builder import builders

discord_color = {
    "red": discord.Colour.red(),
    "yellow": discord.Colour.yellow(),
    "gold": discord.Colour.gold(),
}

def build(con: schema.Container, **kwargs) -> ui.Container:
    # 建構空元件
    container = ui.Container()
    container.accent_color = color(con.accent_color)

    # 將資料物件中的 items 根據類型轉為對應元件
    for index, item_object in enumerate(con.items):

        type_name = item_object.type

        builder = builders.get(type_name)
        if builder is None:
            raise ValueError(f"items[{index}] 有未知的元件類型: {type_name}")

        try:
            container.add_item(builder(item_object, **kwargs))
        except KeyError as e:
            raise ValueError(f"items[{index}] ({type_name}) 缺少必要的屬性: {e}")
        
    return container

def color(value):
    if isinstance(value, str):
        return discord_color.get(value)
    return value or None