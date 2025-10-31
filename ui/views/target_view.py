import discord

from data.command import CommandType

from models.button import ButtonContainer

class TargetView(discord.ui.View):
    def __init__(self, target):
        super().__init__(timeout=None)
        self.target = target

        button_container = ButtonContainer()

        self.add_item(button_container.get_button(CommandType.COMBAT))
        self.add_item(button_container.get_button(CommandType.RETURN))