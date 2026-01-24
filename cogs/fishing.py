import discord
from discord import app_commands
from discord.ext import commands

from context import GUILD_TH_HAVEN, GUILD_AK_BESIM

from session.fishing_session import FishingSession 

class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="釣魚", description="在你所處的地點釣魚")
    async def fishing(self, interaction: discord.Interaction):
        await FishingSession(interaction).start()

async def setup(bot):
    await bot.add_cog(Fishing(bot))