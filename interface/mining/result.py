import discord

class MiningResultEmbed(discord.Embed):
    def __init__(self, user_id: int):
        super().__init__()

        description = [
            "要去哪裡？",
        ]

        self.title = "世界地圖"
        self.description = "\n".join(description)
        self.color = discord.Color.gold()

class MiningResultView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)