import discord
from discord.ext import commands
from discord import app_commands

from game.menus import StatMenu

class StatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="狀態", description="查看你的狀態")
    async def stat(self, interaction: discord.Interaction):
        await StatMenu.show(interaction)

async def setup(bot):
    await bot.add_cog(StatCog(bot))