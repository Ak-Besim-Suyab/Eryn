import discord 
from discord.ext import commands
from discord import app_commands

from interface.region.menu import RegionEmbed, RegionView

from config import GUILD_TH_HAVEN, GUILD_AK_BESIM

class RegionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="地圖", description="打開地圖，前往不同的地點")
    async def region(self, interaction: discord.Interaction):

        embed, view = RegionEmbed(interaction.user.id), RegionView()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(RegionCog(bot))