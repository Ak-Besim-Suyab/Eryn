import discord

class StealView(discord.ui.View):
    view_id = "steal"

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="繼續偷", style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass