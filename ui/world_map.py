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

        info_button = ui.Button(
            label="查看狀態", 
            style=discord.ButtonStyle.secondary,
            custom_id="world_map:info"
        )
        info_button.callback = self.info_button

        guide_button = ui.Button(
            label="查看說明",
            style=discord.ButtonStyle.secondary,
            url="https://suyab42.notion.site/World-Map-41c66f39eca68088b58af76c598047c4",
        )

        self.add_item(ui.ActionRow(info_button, guide_button))

    async def info_button(self, interaction: discord.Interaction):
        info = information.get(interaction.user)
        await interaction.response.send_message(view=view.create("information", **info), ephemeral=True)

class WorldMapConfirm(ui.LayoutView):
    def __init__(self, user: discord.abc.User, destination: str):
        super().__init__(timeout = None)

        self.user = user
        self.destination = REGIONS.get(destination)

        current_region = REGIONS.get(player.get_region(user.id))

        turn = region.get_cost(current_region.id, self.destination.id)

        confirm_button = ui.Button(
            label="確定", 
            style=discord.ButtonStyle.secondary,
            custom_id="world_map:confirm"
        )
        confirm_button.callback = self.confirm_button

        cont = ui.Container()
        cont.add_item(ui.TextDisplay(content = f"## {user.display_name}"))
        cont.add_item(ui.Section(f"從{current_region.name}前往{self.destination.name}將會累積 **{turn}** 回合，確定要前往嗎？", 
                                 accessory=confirm_button))
        cont.add_item(ui.TextDisplay(content = "> -# 若不想進行任何操作，請忽略或刪除這則訊息即可"))

        self.add_item(cont)

    async def confirm_button(self, interaction: discord.Interaction):
        region.move(interaction.user.id, self.destination.id)
        await interaction.response.send_message(f"成功前往{self.destination.name}", ephemeral=True)

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