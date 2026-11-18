import discord
from discord import ui

from data import REGIONS
from data import CONTAINERS

from lib import player
from lib import region
from lib import container
from lib import view
from lib import information

class WorldMap(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout = None)

        self.name = "world_map"

        _select = ui.ActionRow(WorldMapSelect())
        _container = (container
                      .build(CONTAINERS.get("world_map"))
                      .add_item(_select))

        self.add_item(_container)

        info_button = ui.Button(label="查看個人狀態", style=discord.ButtonStyle.secondary)
        info_button.callback = self.info_button

        guide_button = ui.Button(label="查看地圖說明", style=discord.ButtonStyle.secondary)
        guide_button.callback = self.guide_button

        self.add_item(ui.ActionRow(info_button, guide_button))

    async def info_button(self, interaction: discord.Interaction):
        info = information.get(interaction.user)
        await interaction.response.send_message(view=view.create("information", **info), ephemeral=True)

    async def guide_button(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=view.create("map_guide"), ephemeral=True)

class WorldMapConfirm(ui.LayoutView):
    def __init__(self, user: discord.abc.User, destination: str):
        super().__init__(timeout = None)

        self.user = user
        self.destination = destination

        reg_from = REGIONS.get(player.get_region(user.id))
        reg_to = REGIONS.get(destination)

        turn = region.get_cost(reg_from.id, reg_to.id)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"您目前位於**{reg_from.name}**，選擇前往**{reg_to.name}**將會累積 **__{turn}__** 回合，確定要前往嗎？"))

        self.add_item(container)

        confirm_btn = ui.Button(label="確定", style=discord.ButtonStyle.primary)

        self.add_item(ui.ActionRow(confirm_btn))

class WorldMapSelect(ui.Select):
    def __init__(self):

        # 選項列表, 修改列表請調整此參數
        regions = [
            "port_norse", 
            "boreal_forest", 
            "mine"
        ]

        options = []
        for region in regions:
            region = REGIONS.get(region)
            options.append(
                discord.SelectOption(label=region.name,
                                     description=region.description, 
                                     value=region.id)
            )

        super().__init__(
            placeholder = "選擇要前往的地區",
            options = options,
            custom_id = "world_map:select",
        )

    async def callback(self, interaction: discord.Interaction):

        region = REGIONS.get(player.get_region(interaction.user.id))

        if region.id == self.values[0]:
            load = {
                "player_name": interaction.user.display_name,
                "region_name": region.name
            }
            await interaction.response.send_message(view=view.create("map_choose_fail", **load), ephemeral=True)
            return

        await interaction.response.send_message(view=WorldMapConfirm(interaction.user, self.values[0]), ephemeral=True)