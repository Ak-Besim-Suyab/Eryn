import discord

# button style -------------------------------
# discord.ButtonStyle.primary
# discord.ButtonStyle.secondary
# discord.ButtonStyle.success
# discord.ButtonStyle.danger
# discord.ButtonStyle.link
# --------------------------------------------

class BaseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "關於最終幻想",
            emoji = "📜",
            style = discord.ButtonStyle.secondary,
            custom_id = "base_button"
        )

    async def callback(self, interaction: discord.Interaction):
        print("this is a base button!")