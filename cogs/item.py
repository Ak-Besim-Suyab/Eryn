import discord
from discord.ext import commands
from discord import app_commands

from ui.view import OpenableInventory

class ItemCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    item_group = app_commands.Group(name="物品", description="物品的指令集")

    @item_group.command(name="開啟", description="開啟能被打開物品")
    async def search(self, interaction: discord.Interaction, item_name: str = None):
        inventory = OpenableInventory(interaction.user)
        await interaction.response.send_message(view = inventory)

async def setup(bot: commands.Bot):
    await bot.add_cog(ItemCog(bot))