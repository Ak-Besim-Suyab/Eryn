import discord

class MarketView(discord.ui.View):
    id = "market"
    
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="交易", style=discord.ButtonStyle.primary)
    async def trade(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="說明", style=discord.ButtonStyle.secondary)
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass