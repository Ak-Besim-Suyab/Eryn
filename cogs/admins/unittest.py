import discord
from discord.ext import commands
from discord import app_commands

from lib.util.ansi import ANSI, wrap_ansi

class UnitTestCog(commands.Cog):
    """ 
    這個 Cog 用於需要線上運作的單元測試 (例如: 互動元件) 普通單元測試請使用 scripts
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        pass

    @commands.command()
    @commands.is_owner()
    async def ansi(self, ctx: commands.Context):
        text = ANSI("你獲得 50 經驗值").gold()
        ansi_text = wrap_ansi(str(text))

        await ctx.send(ansi_text)

        container = (discord.ui.Container()
                     .add_item(discord.ui.TextDisplay(content = ansi_text)))

        view = (discord.ui.LayoutView(timeout = None)
                .add_item(container))
        
        await ctx.send(view = view)

    @app_commands.command(name="測試", description="測試")
    @app_commands.default_permissions(administrator=True)
    async def unittest_slash(self, interaction: discord.Interaction):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(UnitTestCog(bot))
