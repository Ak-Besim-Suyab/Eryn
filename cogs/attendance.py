import discord
from discord.ext import commands
from discord import app_commands

from game.systems import attendance

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="每日簽到", description="可以領取簽到獎勵")
    async def daily(self, interaction: discord.Interaction):
        await attendance.claim(interaction)

async def setup(bot):
    await bot.add_cog(Daily(bot))