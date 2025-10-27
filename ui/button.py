import discord

from context import Context

class View(discord.ui.View):
    def __init__(self, entry):
        super().__init__(timeout=None)
        self.add_item()

# view 要建立的東西
# button 或 select
# 
class ButtonContainer:
    self.button_excavate_again = discord.ui.Button(label="再次採掘", style=discord.ButtonStyle.primary)