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

        section_keys = [
            ("cabin_overview", "kiki_family"),
            ("cabin_acquisition", "kiki_help"),
            ("cabin_right", "kiki_light"),
            ("cabin_duty", "kiki_sweat"),
        ]

        container = ui.Container()

        # set title.
        title = ui.TextDisplay(content=text.get("cabin_title"))
        container.add_item(title)

        # set content.
        separator = ui.Separator(spacing=SeparatorSpacing.large)
        for text_key, image_key in section_keys:
            section = ui.Section(text.get(text_key), accessory=ui.Thumbnail(media=image.get(image_key)))
            container.add_item(separator)
            container.add_item(section)
        
        # set container to view.
        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AttendanceCog(bot))