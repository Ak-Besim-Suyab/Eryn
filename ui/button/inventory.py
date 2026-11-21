import discord

from lib import information, view

class ResourceButton(discord.ui.Button):
    def __init__(self):

        super().__init__(
            style = discord.ButtonStyle.secondary,
            label = "查看資源",
            custom_id = "inventory:resource"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=view.create("resource_inv", **information.get_resource(interaction.user)), ephemeral=True)