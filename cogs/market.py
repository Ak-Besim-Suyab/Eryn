import discord 
from discord.ext import commands
from discord import app_commands

class MarketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="市集", description="前往港灣後方的市集，購買各式各樣的物品")
    async def execute_market(self, interaction: discord.Interaction):
        pass

async def setup(bot):
    await bot.add_cog(MarketCog(bot))