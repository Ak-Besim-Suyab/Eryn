import discord
from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

from assets import image, text

class AttendanceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 使用傳統指令，避免只用指令時顯示的訊息標註指令使用者
    @commands.command()
    async def attendance(self, ctx: commands.Context):
        await ctx.send(view=AttendanceView())

class AttendanceView(ui.LayoutView):

    """由於該視圖 (View) 需要做持久性 (Persistent) 處理, 因此不會將其縮限至工廠函式"""

    def __init__(self):
        super().__init__(timeout=None)

        container = ui.Container()

        # 標題
        title = ui.TextDisplay(content="## 每日簽到")
        container.add_item(title)

        # 文本
        text.reload()
        overview = ui.Section(text.get("attendance_overview"), accessory=ui.Thumbnail(media=image.get("kiki_with_gf")))
        container.add_item(overview)

        separator = ui.Separator(spacing=SeparatorSpacing.large)
        container.add_item(separator)

        buttons = [
            ("簽到", discord.ButtonStyle.primary, "🎁", "attendance:claim"),
            ("狀態", discord.ButtonStyle.secondary, "▫️", "attendance:stat"),
            ("排名", discord.ButtonStyle.secondary, "▫️", "attendance:leaderboard"),
            ("說明", discord.ButtonStyle.secondary, "❓", "guide:attendance"),
        ]

        row = ui.ActionRow()
        for label, style, emoji, custom_id in buttons:
            button = ui.Button(label=label, style=style, emoji=emoji, custom_id=custom_id)
            row.add_item(button)
        container.add_item(row)

        # set container to view.
        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AttendanceCog(bot))