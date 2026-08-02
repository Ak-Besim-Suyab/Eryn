import discord
from discord import ui
from discord import SeparatorSpacing
from discord.ext import commands

from assets import text, image

separator = ui.Separator(spacing=SeparatorSpacing.large)

async def attendance(interaction: discord.Interaction):

    container = ui.Container()

    title = ui.TextDisplay(content=f"## 每日簽到指南")
    container.add_item(title)

    container.add_item(separator)

    text.reload()
    content = ui.TextDisplay(content=text.get("guide_attendance"))
    container.add_item(content)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)

async def tavern(ctx: commands.Context):

    text.reload()
    texts = text.get("guide_tavern")
    if not isinstance(texts, dict):
        raise TypeError("Error: guide_tavern.yaml is not a dict format.")

    # 標題區塊
    container = ui.Container()
    container.add_item(ui.TextDisplay(content=texts.get("title")))
    container.add_item(ui.Section(texts.get("overview"), accessory=ui.Thumbnail(image.get("did_feast_1"))))
    container.add_item(separator)

    option = ui.ActionRow()
    option.add_item(Select())
    container.add_item(option)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)

    await ctx.send(view=view, ephemeral=True)

async def tavern_post(interaction: discord.Interaction) -> None:

    text.reload()
    texts = text.get("guide_tavern")
    if not isinstance(texts, dict):
        raise TypeError("Error: guide_tavern.yaml is not a dict format.")

    container = ui.Container()
    container.add_item(ui.TextDisplay(content=texts.get("post_title")))
    container.add_item(ui.Section(texts.get("post_description"), accessory=ui.Thumbnail(image.get("did_feast_2"))))

    view = ui.LayoutView(timeout=None)
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)

async def tavern_discussion(interaction: discord.Interaction) -> None:

    text.reload()
    texts = text.get("guide_tavern")
    if not isinstance(texts, dict):
        raise TypeError("Error: guide_tavern.yaml is not a dict format.")

    button = ui.Button(label="社群守則", url="https://discord.com/channels/1190027756482859038/1509068887768174633", emoji="📜")

    container = ui.Container()
    container.add_item(ui.TextDisplay(content=texts.get("discussion_title")))
    container.add_item(ui.Section(texts.get("discussion_description"), accessory=ui.Thumbnail(image.get("did_feast_2"))))
    container.add_item(separator)

    row = ui.ActionRow()
    row.add_item(button)
    container.add_item(row)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)

async def tavern_channel(interaction: discord.Interaction) -> None:

    text.reload()
    texts = text.get("guide_tavern")
    if not isinstance(texts, dict):
        raise TypeError("Error: guide_tavern.yaml is not a dict format.")

    container = ui.Container()
    container.add_item(ui.TextDisplay(content=texts.get("channel_title")))
    container.add_item(ui.Section(texts.get("channel_description"), accessory=ui.Thumbnail(image.get("did_feast_3"))))
    container.add_item(separator)

    gallery = ui.MediaGallery()
    gallery.add_item(media="https://cdn.discordapp.com/attachments/1491046495812718672/1532454816087933059/2026-07-31_022221.png")
    container.add_item(gallery)

    view = ui.LayoutView(timeout=None)
    view.add_item(container)



    await interaction.response.send_message(view=view, ephemeral=True)

class Select(ui.Select):
    def __init__(self):

        pools = [
            ("🍹發文時需要注意什麼？", "tavern_post"),
            ("🍹討論時需要注意什麼？", "tavern_discussion"),
            ("🍹如何將貼文顯示在列表？", "tavern_channel")
        ]

        options = []
        for label, value in pools:
            option = discord.SelectOption(label=label, value=value)
            options.append(option)

        super().__init__(
            placeholder="請選擇想閱讀的指南", 
            min_values=1, 
            max_values=1, 
            options=options
        )