from discord.ext import commands
from discord import ui

class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        await ctx.send(view=TestView())

class TestView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))