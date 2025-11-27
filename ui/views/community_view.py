import discord
from context import Context

class CommunityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button_manager = Context.get_manager("button")
        self.add_item(button_manager.create("community_rule_button"))