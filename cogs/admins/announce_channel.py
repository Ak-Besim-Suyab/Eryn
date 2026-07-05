from discord.ext import commands
from discord import ui
from discord import SeparatorSpacing

from assets import image, text

class AnnounceChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def announce_channel(self, ctx: commands.Context):
        await ctx.send(view=AnnounceChannelView())

class AnnounceChannelView(ui.LayoutView):
    
    """由於該視圖 (View) 需要做持久性 (Persistent) 處理, 因此不會將其縮限至工廠函式"""
    
    def __init__(self):
        super().__init__(timeout=None)

        container = ui.Container()

        title = ui.TextDisplay(content=text.get("channel_title"))
        overview = ui.TextDisplay(content=text.get("channel_overview"))

        container.add_item(title)
        container.add_item(overview)

        section_key = [
            ("channel_camping", "camping"),
            ("channel_river", "port"),
            ("channel_aquarium", "aquarium"),
            ("channel_street", "street"),
            ("channel_coffee", "coffee"),
        ]

        separator = ui.Separator(spacing=SeparatorSpacing.large)
        for text_key, image_key in section_key:
            section = ui.Section(text.get(text_key), accessory=ui.Thumbnail(media=image.get(image_key)))
            container.add_item(separator)
            container.add_item(section)

        self.add_item(container)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceChannelCog(bot))