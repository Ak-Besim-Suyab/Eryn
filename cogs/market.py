import discord 
from discord.ext import commands
from discord import app_commands

from game import ui

class MarketCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="市集", 
        description="前往港灣後方的市集，購買各式各樣的物品")
    async def start(self, interaction: discord.Interaction):
        # embed, view = ui.Embed(), ui.View()
        # await interaction.response.send_message(embed=embed, view=view)
        """"""
        
async def setup(bot: commands.Bot):
    await bot.add_cog(MarketCog(bot))