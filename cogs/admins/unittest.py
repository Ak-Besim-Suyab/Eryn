import discord
from discord.ext import commands
from discord import app_commands

import data
from lib import player

from lib.view import create_view

class UnitTestCog(commands.Cog):
    """ 這個 Cog 用於需要傳入互動元件的單元測試, 普通單元測試請到 scripts 進行編寫
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def unittest_legacy(self, ctx: commands.Context):
        pass

    @app_commands.command(name="測試", description="測試用指令")
    @app_commands.default_permissions(administrator=True)
    async def unittest_slash(self, interaction: discord.Interaction):
        view = create_view("template")
        await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnitTestCog(bot))
