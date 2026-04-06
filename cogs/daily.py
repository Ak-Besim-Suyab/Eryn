import discord
from discord.ext import commands
from discord import app_commands

from systems.reward_service import RewardService

from configuration import GUILD_TH_HAVEN, GUILD_AK_BESIM

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="每日獎勵", description="領取每日獎勵")
    async def daily(self, interaction: discord.Interaction):
        await RewardService().claim(interaction)

async def setup(bot):
    await bot.add_cog(Daily(bot))