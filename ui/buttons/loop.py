import discord

class PetAgainButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "關於最終幻想",
            emoji = "📜",
            style = discord.ButtonStyle.secondary,
            custom_id = "base_button"
        )