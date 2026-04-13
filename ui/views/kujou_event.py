import discord

class KujouEventView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="緬懷", style=discord.ButtonStyle.primary, emoji="🕯️", custom_id="mourn")
    async def mourn(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="供奉", style=discord.ButtonStyle.primary, emoji="🕯️", custom_id="season_offer")
    async def season_offer(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="說明", style=discord.ButtonStyle.secondary, custom_id="season_event_intro")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass