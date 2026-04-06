import discord

# 這裡導入需要的 Model
from models.player import Player
from models.region import region_manager
from models.resource import resource_manager

# 這裡導入按鈕，並在 MenuView 添加
from interface.action.option import ActionOption

class MenuEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        region = region_manager.get(Player.get_region(interaction.user.id))

        self.color = discord.Color.gold()
        self.add_field(name="你目前在：", value=f"- {region.name}", inline=False)

        resources = region.resources
        resource_table = []
        if resources is not None:
            for res in resources:
                resource = resource_manager.get(res)
                resource_table.append(f"- {resource.name}")
            
            self.add_field(name="找到資源：", value="\n".join(resource_table), inline=False)
        else:
            self.add_field(name="沒有找到任何資源。", value="", inline=False)

        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(ActionOption())