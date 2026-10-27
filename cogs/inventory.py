import discord
from discord.ext import commands
from discord import app_commands

from ui.view import InventoryView

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="背包", description="打開物品欄查看道具")
    async def inventory(self, interaction: discord.Interaction):
        inventory = InventoryView(interaction.user)
        await interaction.response.send_message(view = inventory)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryCog(bot))