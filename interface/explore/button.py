import discord

from models.player import Player
from models.region import region_manager
from models.resource import resource_manager

class ExploreButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.primary, 
            label="探索", 
            emoji="🔍", 
            custom_id="explore"
        )
    
    async def callback(self, interaction: discord.Interaction):
        region = region_manager.get_region(Player.get_region(interaction.user.id))

        embed = discord.Embed()
        embed.description = f"你在{region.name}進行探索，環顧周遭後..."
        embed.title = interaction.user.display_name

        resources = region.resources

        resource_table = []
        
        if resources is not None:
            for res in resources:
                resource = resource_manager.get_resource(res)
                resource_table.append(f"- {resource.name}")
            
            embed.add_field(name="找到資源：", value="\n".join(resource_table), inline=False)
        else:
            embed.add_field(name="沒有找到任何資源。", value="", inline=False)

        await interaction.response.send_message(embed=embed)