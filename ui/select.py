import discord

class LookSelect(discord.ui.Select):
    def __init__(self, data: list):

        options = [discord.SelectOption(label=d["name"], value=d, emoji="") for d in data]

        super().__init__(placeholder = "請選擇", options = options, min_values = 1, max_values = 1)