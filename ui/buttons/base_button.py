import discord

class BaseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "測試",
            emoji = "📜",
            style = discord.ButtonStyle.primary,
            custom_id = "base_button"
        )

    async def callback(self, interaction: discord.Interaction):
        print("this is a base button!")