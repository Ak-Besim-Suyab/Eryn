import discord

from cogs.inventory import build_inventory_embed, InventoryActionView


class BackToInventoryButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="返回", 
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        embed = build_inventory_embed(interaction.user)
        await interaction.response.edit_message(
            embed=embed,
            view=InventoryActionView()
        )