import discord

from lib import information
from lib import view

class StatButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="查看個人狀態", 
            custom_id="stat"
        )

    async def callback(self, interaction: discord.Interaction):
        info = information.get(interaction.user)
        v = view.create("information", **info)
        await interaction.response.send_message(view=v, ephemeral=True)