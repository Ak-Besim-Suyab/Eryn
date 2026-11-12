import discord
from discord import ui

from data import REGIONS
from lib import player, region
from ui.view import RegionConfirmView

class RegionSelect(ui.Select):
    def __init__(self):

        regions = {"haven", "boreal_forest", "mine"}

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