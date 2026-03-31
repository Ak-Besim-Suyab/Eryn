import discord

class RegionSuccessEmbed(discord.Embed):
    def __init__(self, player_name: str, region_name: str):
        super().__init__()

        self.title = player_name
        self.description = f"成功到達{region_name}"
        self.color = discord.Color.gold()