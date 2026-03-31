import discord

from interface.vendor import VendorEmbed, VendorView

class TradeEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        description = [
            "> 你在街道上漫步行進，奶酪與蜂蜜陳列、布袍與獸皮成堆。",
            "> 數個攤販正在出售的物品讓你很感興趣，你試著湊近點並開始他們詢問。"
        ]

        value = [
            "- 雜貨商",
            "- 紋章官（身分組）",
        ]

        self.title = interaction.user.display_name
        self.description = "\n".join(description)
        self.color = discord.Color.gold()
        self.add_field(name="選擇以下對象開始進行交易：", value="\n".join(value))


class TradeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

        self.add_item(TradeOption())


class TradeOption(discord.ui.Select):
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