import discord
from discord import ui

from data import REGIONS
from lib import player, region

class RegionConfirmView(ui.LayoutView):
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

class RegionSelect(ui.Select):
    def __init__(self):

        # 選項列表, 修改列表請調整此參數
        regions = {"port_norse", "boreal_forest", "mine"}

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
        )

    async def callback(self, interaction: discord.Interaction):

        region = REGIONS.get(player.get_region(interaction.user.id))

        if region.id == self.values[0]:

            container = ui.Container()
            container.add_item(ui.TextDisplay(content = f"> *你覺得在{region.name}原地打轉還蠻有意思（無法移動，原因：選擇和所處地點相同的位置）*"))

            view = ui.LayoutView(timeout = None)
            view.add_item(container)

            await interaction.response.send_message(view=view)
            return

        await interaction.response.send_message(view=RegionConfirmView(interaction.user, self.values[0]))

