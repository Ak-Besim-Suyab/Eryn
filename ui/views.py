import discord
from discord import ui

from ui.select import RoleSelect

class RoleSettingView(discord.ui.LayoutView):
    """
    通用裝飾身分組設定面板
    """
    def __init__(self, title: str, media: str, tag: str):
        super().__init__(timeout=None)

        select = RoleSelect(custom_id=f"{tag}_role_select", tag=tag)

        c = discord.ui.Container()

        if media:
            c.add_item(discord.ui.MediaGallery().add_item(media=media))
            c.add_item(discord.ui.Separator(spacing=discord.SeparatorSpacing.large))

        c.add_item(discord.ui.TextDisplay(f"## {title}"))
        c.add_item(discord.ui.TextDisplay("> 請注意，相同分類的身分組同時只能套用 1 個"))
        c.add_item(ui.ActionRow(select))

        self.add_item(c)

class FishingEventView(discord.ui.LayoutView):
    """
    釣魚大成功時觸發的特殊事件面板
    """
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)

        c = discord.ui.Container()
        c.add_item(discord.ui.TextDisplay(content=f"### {interaction.user.display_name}"))
        c.add_item(discord.ui.TextDisplay(content="你察覺到河裡有什麼正在閃耀著"))

        inspect_btn = discord.ui.Button(label="查看", style=discord.ButtonStyle.secondary)
        inspect_btn.callback = self.on_inspect

        self.add_item(c)
        self.add_item(ui.ActionRow(inspect_btn))

    async def on_inspect(self, interaction: discord.Interaction):
        c = discord.ui.Container()
        c.add_item(discord.ui.TextDisplay(content="你發現魚群聚集點！"))

        v = discord.ui.LayoutView()
        v.add_item(c)

        await interaction.response.send_message(view=v)
