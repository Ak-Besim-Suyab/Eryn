import discord

from models.player.model import Player
from models.region import region_manager

from interface.region.option_success import RegionSuccessEmbed
from interface.region.option_overlap import RegionOverlapEmbed

class RegionEmbed(discord.Embed):
    def __init__(self, user_id: int):
        super().__init__()

        description = [
            "要去哪裡？",
        ]

        self.title = "世界地圖"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()
    
        current_region = Player.get_region(user_id)
        region = region_manager.get(current_region)

        self.add_field(name="你目前在：", value=region.name, inline=False)

class RegionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(RegionOption())

class RegionOption(discord.ui.Select):
    def __init__(self):

        regions = region_manager.get_all()

        options = []
        for region in regions:
            option = discord.SelectOption(label=region.name, value=region.id, description="選擇後將前往目的地")
            options.append(option)

        super().__init__(
            placeholder="請選擇要前往的地區", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        region = region_manager.get(self.values[0])
        player_name = interaction.user.display_name
        region_name = region.name

        if Player.get_region(interaction.user.id) != region.id:
            Player.set_region(interaction.user.id, region.id)
            embed = RegionSuccessEmbed(player_name=player_name, region_name=region_name)
        else:
            embed = RegionOverlapEmbed(player_name=player_name, region_name=region_name)

        await interaction.response.edit_message(embed=embed, view=None)