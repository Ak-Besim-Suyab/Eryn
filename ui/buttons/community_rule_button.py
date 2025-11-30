import discord

class CommunityRuleButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "社群規範",
            emoji = "📜",
            style = discord.ButtonStyle.secondary, 
            custom_id = "community_rule"
        )

    async def callback(self, interaction: discord.Interaction):
        lines = [
            "# 📜 社群規範",
            "Th Haven 致力於提供給每位旅人良好的遊戲與交流環境；為此，希望旅人都能共同遵守社群規範，以維護善良風氣。",
            "有任何事情發生時，請務必優先聯絡管理員，切勿私自解決；同時，管理員會對事件進行評估，並根據情節程度決定如何處理。",
        ]

        embed = discord.Embed(
            title = "# 📜 社群規範",
            description = "\n".join(lines),
            color = discord.Color.blue()
        )

        view = View()

        await interaction.response.send_message(
            embed = embed,
            view = view,
            ephemeral = True
        )

class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button())

class Button(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "對話", style = discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        print("this is dialogue button!")