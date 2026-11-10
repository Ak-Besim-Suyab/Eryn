import discord
from discord import ui

from data import REGIONS
from lib import region

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
        success, line = region.move(interaction.user.id, self.values[0])
        container = (ui.Container()
                     .add_item(ui.TextDisplay(content=line))
        )
        view = (ui.LayoutView()
                .add_item(container)
        )
        await interaction.response.send_message(view=view)