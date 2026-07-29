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

    view = ui.LayoutView()
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

    view = ui.LayoutView()
    view.add_item(container)

    await ctx.send(view=view, ephemeral=True)

async def tavern_rule(interaction: discord.Interaction):

    text.reload()
    texts = text.get("guide_tavern")
    if not isinstance(texts, dict):
        raise TypeError("Error: guide_tavern.yaml is not a dict format.")

    container = ui.Container()
    container.add_item(ui.TextDisplay(content=texts.get("rule_title")))
    container.add_item(separator)
    container.add_item(ui.Section(texts.get("rule_overview"), accessory=ui.Thumbnail(image.get("did_feast_2"))))
    container.add_item(separator)
    container.add_item(ui.TextDisplay(content=texts.get("rule_1")))
    container.add_item(separator)
    container.add_item(ui.TextDisplay(content=texts.get("rule_2")))

    view = ui.LayoutView()
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)

class Select(ui.Select):
    def __init__(self):

        pools = [
            ("🍷小酒館發文與討論須知", "option_1"),
            ("🍷如何將貼文顯示在列表？", "option_2")
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
    
    async def callback(self, interaction: discord.Interaction):
        match self.values[0]:
            case "option_1":
                return await tavern_rule(interaction)
            case "option_2":
                return await interaction.response.send_message("關於如何將貼文顯示在列表上", ephemeral=True)
        pass