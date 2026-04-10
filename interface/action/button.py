import discord
from systems.commands.garden import garden_skill

class GardenButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.primary, 
            label="採集", 
            emoji="🌿", 
            custom_id="garden"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await garden_skill.cast(interaction)