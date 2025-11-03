import discord

from data.command import CommandType

from ui.button import ButtonManager

class TargetView(discord.ui.View):
    def __init__(self, target):
        super().__init__(timeout=None)
        self.target = target

        button_manager = ButtonManager()

        self.add_item(button_manager.get_button(CommandType.COMBAT))
        self.add_item(button_manager.get_button(CommandType.RETURN))