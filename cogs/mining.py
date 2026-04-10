import discord 
from discord.ext import commands
from discord import app_commands

from interface.region.menu import RegionEmbed, RegionView

from config import GUILD_TH_HAVEN, GUILD_AK_BESIM

class MiningCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="挖掘", description="在你目前所處的地點挖掘，獲得相關資源")
    async def mining(self, interaction: discord.Interaction):

        embed, view = RegionEmbed(interaction.user.id), RegionView()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(MiningCog(bot))