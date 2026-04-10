import discord
from discord.ext import commands
from discord import app_commands

from models.data.item import item_manager
from models.inventory import Inventory
from models.message import message_manager

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="背包", description="查看自己的背包")
    async def inventory(self, interaction: discord.Interaction):

        inventory = Inventory.get_inventory(interaction.user.id)

        inventory_value = []
        if inventory:
            for item_id, quantity in inventory.items():
                item = item_manager.get(item_id)
                inventory_value.append(f"{item.image}{item.name} x{quantity}")
        else:
            inventory_value.append("*尚未擁有任何物品*")

        newline = "\n"
        payload = {"inventory_value": newline.join(inventory_value)}

        embed = message_manager.create("inventory", payload=payload, interaction=interaction)
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(InventoryCog(bot))