import discord
from discord import ui
from discord import SeparatorSpacing

class Information:

    @staticmethod
    async def show(interaction: discord.Interaction):
        await interaction.response.send_message(view=InformationView(), ephemeral=True)
        
class InformationView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        container = ui.Container()

        self.add_item(container)

# singletons declaration ---------------------------------------

_instance = Information()

show = _instance.show