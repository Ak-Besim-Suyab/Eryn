import discord

# 這裡導入需要的 Model
from models.player import Player
from models.region import region_manager

# 這裡導入按鈕，並在 MenuView 添加
from interface.explore.button import ExploreButton
from interface.action.button import GardenButton

class MenuEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        region = region_manager.get_region(Player.get_region(interaction.user.id))

        self.color = discord.Color.gold()
        self.add_field(name="你目前在：", value=region.name, inline=False)
        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(ExploreButton())
        self.add_item(GardenButton())