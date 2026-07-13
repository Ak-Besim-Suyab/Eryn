import discord
from discord import ui
from discord import SeparatorSpacing

from assets import text

async def attendance(interaction: discord.Interaction):

    container = ui.Container()

    title = ui.TextDisplay(content=f"## 每日簽到指南")
    container.add_item(title)

    separator = ui.Separator(spacing=SeparatorSpacing.large)
    container.add_item(separator)

    text.reload()
    content = ui.TextDisplay(content=text.get("guide_attendance"))
    container.add_item(content)

    view = ui.LayoutView()
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)

async def tavern(interaction: discord.Interaction):

    container = ui.Container()

    title = ui.TextDisplay(content=f"## 酒館指南")
    container.add_item(title)

    view = ui.LayoutView()
    view.add_item(container)

    await interaction.response.send_message(view=view, ephemeral=True)