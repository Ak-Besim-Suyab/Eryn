import discord
from discord.ext import commands
from discord import app_commands

from models.data.item import item_manager
from models.inventory import Inventory
from configuration import GUILD_AK_BESIM, GUILD_TH_HAVEN

inventory_img = "https://cdn.discordapp.com/attachments/1193049715638538283/1481102388021690530/inventory_img.png"

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="背包", description="查看你的背包")
    async def inventory(self, interaction: discord.Interaction):

        inventory = Inventory.get_inventory(interaction.user.id)

        item_descriptions = []

        if inventory:
            for item_id, quantity in inventory.items():
                item = item_manager.get(item_id)
                item_descriptions.append(f"{item.name} x{quantity}")
        else:
            item_descriptions.append("*尚未擁有任何物品*")
        
        embed = discord.Embed()
        embed.color = discord.Color.dark_gold()
        embed.set_author(name=f"{interaction.user.display_name}的背包", icon_url=interaction.user.avatar.url)
        embed.set_image(url=inventory_img)

        embed.add_field(name="", value="\n".join(item_descriptions), inline=False)

        await interaction.response.send_message(embed=embed)
    

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))