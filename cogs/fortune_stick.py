import random
import discord
from discord.ext import commands
from discord import app_commands

sticks = [
    "<:dai_kichi:1561975565500817428>",
    "<:kichi:1561975597335314542>",
    "<:sho_kichi:1561975608949481542>",
    "<:sho_kyo:1561975734153781318>",
    "<:kyo:1561975744417239050>",
    "<:dai_kyo:1561975786398023780>"
]

class FortuneStickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="抽籤", description="使用後會隨機抽取幸運籤")
    @app_commands.describe(moves="抽籤次數（選填）")
    async def fortune_stick(self, interaction: discord.Interaction, moves: int = 1):

        turns = []
        
        for _ in range(moves):
            turns.append(random.choice(sticks))

        await interaction.response.send_message(''.join(turns))

async def setup(bot: commands.Bot):
    await bot.add_cog(FortuneStickCog(bot))
