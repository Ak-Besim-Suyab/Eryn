import discord
from discord.ext import commands
from discord import app_commands

from game.menus import StatMenu

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="資訊", description="查看旅人的社群資訊")
    async def info_command(self, interaction: discord.Interaction):
        await StatMenu.show(interaction)

async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))