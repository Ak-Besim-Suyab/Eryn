import discord
from systems.skills.garden import GardenSkill

class GardenButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.primary, 
            label="再次採集", 
            emoji="🌿", 
            custom_id="garden"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await GardenSkill.cast(interaction)