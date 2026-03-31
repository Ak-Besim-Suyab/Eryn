import discord

class GuideEmbed(discord.Embed):
    def __init__(self):
        super().__init__()

        description = [
            "　*這是本用於介紹避風港的手冊，新進旅人請務必閱讀，以便瞭解社群的所有功能與規定。*",
        ]

        self.title = "《旅居手冊》"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()

class GuideView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(GuideOption())

class GuideOption(discord.ui.Select):
    def __init__(self):

        options = []

        labels = [
            "社群規範",
            "頻道介紹",
            "小屋系統",
        ]

        for label in labels: 
            option = discord.SelectOption(
                label=label,
                description="選擇後開始閱讀"
            )

        super().__init__(
            placeholder="請選擇想閱讀的章節", 
            min_values=1, 
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        match self.values[0]:
            case "社群規範":
                await interaction.response.send_message("社群規範", ephemeral=True)
            case "頻道介紹":
                await interaction.response.send_message("頻道介紹", ephemeral=True)
            case "小屋系統":
                await interaction.response.send_message("小屋系統", ephemeral=True)