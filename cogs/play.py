import discord
from discord.ext import commands
from discord import app_commands
import random

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Cogs] Command /play loaded.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="play", description="開始遊玩 Eryn")
    async def play(self, interaction: discord.Interaction):
        action = ["戰鬥", "採掘", "捕獲動物", "釣魚"]

        embed = discord.Embed(
                    title=f"{interaction.user.display_name}，歡迎回來！",
                    description=f"今天感覺會是個**{random.choice(action)}**的好日子（未實裝）",
                    color=discord.Color.greyple()
                )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1193049715638538283/1429993112633085963/Bakery_pixel_art3.png")
        embed.add_field(name="要做什麼呢？", value="", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))