import discord
import game
from game import model
from game import ui

class View(discord.ui.View):
    def __init__(self, model: model.View, context: game.Context):

        self.model = model

        super().__init__(timeout=model.timeout)

        if model.buttons:
            for button in model.buttons:
                btn = ui.Button(button)
                self.add_item(btn)
        
        if model.selects:
            for select in model.selects:
                sel = ui.Select(select)
                self.add_item(sel)