import discord

from interface.vendor import VendorEmbed, VendorView

class MarketChooseView(discord.ui.View):
    id = "market_choose"

    def __init__(self):
        super().__init__(timeout=300)

        self.add_item(MarketChooseOption())


class MarketChooseOption(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="雜貨商", description="在集市中購買雜物"),
            discord.SelectOption(label="紋章官（身分組）", description="在集市中購買紋章（身分組）"),
        ]
        super().__init__(placeholder="選擇對象", options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        match self.values[0]:
            case "雜貨商":
                await self.vendor(interaction)
            case "紋章官（身分組）":
                await self.herald(interaction)

    async def vendor(self, interaction: discord.Interaction):
        embed, view = VendorEmbed(), VendorView()
        await interaction.response.send_message(embed=embed, view=view)

    async def herald(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.title = "紋章官（身分組）"
        embed.description = "功能尚未開放，敬請期待！"
        embed.color = discord.Color.gold()

        await interaction.response.send_message(embed=embed)