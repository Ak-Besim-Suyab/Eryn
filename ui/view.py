import discord

class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class TargetView(discord.ui.View):
    def __init__(self, target):
        super().__init__(timeout=None)
        self.target = target