import discord
from discord.ext import commands
from discord import app_commands

from views import inventory

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="背包", description="查看自己的背包")
    async def inventory(self, interaction: discord.Interaction):
        await inventory.InventoryMenu().show(interaction)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryCog(bot))