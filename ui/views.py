import discord
from discord import ui

from ui.select import RoleSelect


class RoleSettingView(discord.ui.LayoutView):
    """通用裝飾身分組設定面板"""

    def __init__(self, title: str, media: str, pool: str):
        super().__init__(timeout=None)

        select = RoleSelect(custom_id=f"{pool}_role_select", tag=pool)

        c = discord.ui.Container()

        if media:
            c.add_item(discord.ui.MediaGallery().add_item(media=media))
            c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(discord.ui.TextDisplay(f"## {title}"))
        c.add_item(discord.ui.TextDisplay("請注意：相同類型的身分組同時只會套用 1 個"))
        c.add_item(ui.ActionRow(select))

        self.add_item(c)
