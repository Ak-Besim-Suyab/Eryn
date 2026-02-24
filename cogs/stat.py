import discord
from discord.ext import commands
from discord import app_commands

from systems.stat_service import StatService

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

class Stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="狀態", description="查看你的角色狀態")
    async def stat(self, interaction: discord.Interaction):
        await StatService().view(interaction)

async def setup(bot):
    await bot.add_cog(Stat(bot))