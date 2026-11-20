import discord

class InventoryButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="背包", style=discord.ButtonStyle.secondary)