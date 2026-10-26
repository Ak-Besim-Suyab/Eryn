import random
import discord
from discord.ext import commands
from discord import app_commands

from config import SIGN_POOL

class RPSCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="猜拳", description="使用後會隨機出拳")
    @app_commands.describe(moves="出拳次數（選填）")
    async def rock_paper_scissors(self, interaction: discord.Interaction, moves: int = 1):

        turns = []
        for _ in range(moves):
            turns.append(random.choice(SIGN_POOL))

        await interaction.response.send_message(''.join(turns))

async def setup(bot: commands.Bot):
    await bot.add_cog(RPSCog(bot))
