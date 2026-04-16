import discord
from models.player import Player
from models.inventory import Inventory
from models.item import item_registry

class InventoryMenu:
    @staticmethod
    async def show(interaction: discord.Interaction):

        player = Player.get_or_create_player(interaction.user.id)
        inventory = Inventory.get_inventory(interaction.user.id)

        currency_text = []
        inventory_value = []

        if hasattr(player, "currency"):
            currency_text.append(f"{player.currency} 金幣")

        if inventory:
            for item_id, quantity in inventory.items():
                item = item_registry.get(item_id)
                inventory_value.append(f"{item.image}{item.name} x{quantity}")
        else:
            inventory_value.append("*尚未擁有任何物品*")

        embed = discord.Embed()
        embed.color = discord.Color.gold()

        embed.add_field(name="持有貨幣：", value="\n".join(currency_text), inline=False)
        embed.add_field(name="持有物品：", value="\n".join(inventory_value), inline=False)

        await interaction.response.send_message(embed=embed)