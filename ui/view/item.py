import discord
from discord import ui

import data

class ItemView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, item_id: str, quantity: int = 1):
        super().__init__(timeout = None)
        self.user = user
        self.item_id = item_id
        self.quantity = quantity

        self.render()

    def render(self):
        item = data.item.get(self.item_id)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name}"))
        container.add_item(ui.TextDisplay(content = item.name))

        self.add_item(container)