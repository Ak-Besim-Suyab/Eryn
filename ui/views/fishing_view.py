import discord

from context import Context

class FishingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        button_manager = Context.get_manager("button")

        # attach buttons
        self.add_item(button_manager.create("fishing_again_button"))
        self.add_item(button_manager.create("back_to_inventory_button"))