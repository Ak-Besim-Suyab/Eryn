import discord

class ExploredEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

