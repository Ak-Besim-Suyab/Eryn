import discord

class RegionOverlapEmbed(discord.Embed):
    def __init__(self, player_name: str, region_name: str):
        super().__init__()

        self.title = player_name
        self.description = f"你本來就在{region_name}，在想什麼呢？"
        self.color = discord.Color.gold()