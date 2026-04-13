import discord

class PreOfferView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="確定", style=discord.ButtonStyle.primary, custom_id="season_offer_confirm")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
    
    @discord.ui.button(label="取消", style=discord.ButtonStyle.secondary, custom_id="season_offer_cancel")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass