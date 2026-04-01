import discord
from systems.skills.garden import GardenSkill

class GardenButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.primary, 
            label="採集", 
            emoji="🌿", 
            custom_id="garden"
        )
    
    async def callback(self, interaction: discord.Interaction):
        result = GardenSkill.cast(interaction.user.id)
        await interaction.response.send_message("你前往附近的花園，開始採集資源... (製作中)", ephemeral=True)