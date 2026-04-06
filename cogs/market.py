import discord 
from discord.ext import commands
from discord import app_commands

from interface.market import MarketEmbed, MarketView

from configuration import GUILD_TH_HAVEN, GUILD_AK_BESIM

class MarketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="市集", description="前往港灣後方的市集，購買各式各樣的物品")
    async def market(self, interaction: discord.Interaction):

        embed = MarketEmbed()
        view = MarketView()

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(MarketCog(bot))