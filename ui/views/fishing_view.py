import discord

class FishingView(discord.ui.View):
    def __init__(self, session):
        super().__init__(timeout=300)
        self.session = session

    @discord.ui.button(label="繼續釣", style=discord.ButtonStyle.primary)
    async def repeat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.session.start(interaction)