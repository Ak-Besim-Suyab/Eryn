import discord
from discord.ext import commands
from discord import app_commands

from models.data.item import item_manager
from models.inventory import Inventory
from models.message import message_manager
from configuration import GUILD_AK_BESIM, GUILD_TH_HAVEN

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="背包", description="查看你的背包")
    async def inventory(self, interaction: discord.Interaction):

        inventory = Inventory.get_inventory(interaction.user.id)

        inventory_value = []
        if inventory:
            for item_id, quantity in inventory.items():
                item = item_manager.get(item_id)
                inventory_value.append(f"{item.name} x{quantity}")
        else:
            inventory_value.append("*尚未擁有任何物品*")
        
        payload = {
            "inventory_value": "\n".join(inventory_value)
        }

        embed = message_manager.create("inventory", payload=payload, user=interaction.user)

        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(InventoryCog(bot))