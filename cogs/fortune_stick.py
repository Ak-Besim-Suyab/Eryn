import random
import discord
from discord.ext import commands
from discord import app_commands

from config import OMIKUJI_POOL

class FortuneStickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="抽籤", description="使用後會隨機抽取幸運籤")
    @app_commands.describe(moves="抽籤次數（選填）")
    async def fortune_stick(self, interaction: discord.Interaction, moves: int = 1):

        turns = []
        for _ in range(moves):
            turns.append(random.choice(OMIKUJI_POOL))

        await interaction.response.send_message(''.join(turns))

async def setup(bot: commands.Bot):
    await bot.add_cog(FortuneStickCog(bot))
