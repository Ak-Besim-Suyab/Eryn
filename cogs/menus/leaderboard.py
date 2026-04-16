import discord
from discord.ext import commands
from discord import app_commands

from game.menus import LeaderboardMenu

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="排名", description="查看成員排名")
    async def execute(self, interaction: discord.Interaction):
        await LeaderboardMenu.show(interaction)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))