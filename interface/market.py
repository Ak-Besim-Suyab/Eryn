import discord

from interface.trade import TradeEmbed, TradeView

class MarketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="交易", style=discord.ButtonStyle.primary)
    async def trade(self, interaction: discord.Interaction, button: discord.ui.Button):

        embed = TradeEmbed(interaction)
        view = TradeView()

        await interaction.response.send_message(embed=embed, view=view)

    @discord.ui.button(label="說明", style=discord.ButtonStyle.secondary)
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        embed = discord.Embed()
        embed.title = "Elin"
        embed.description = "「這裡是市集喵，你可以在這裡進行各種買賣。購買身分組也在此進行，旅人可以在這裡發掘有趣的身分組。」"
        embed.color = discord.Color.gold()
        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        await interaction.response.send_message(embed=embed)