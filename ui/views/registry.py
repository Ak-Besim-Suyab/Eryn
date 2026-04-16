import discord

class ViewRegistry:
    def __init__(self):
        self.views: dict[str, discord.ui.View] = {}

    def register(self, view_id: str, view: discord.ui.View):
        self.views[view_id] = view

    def get(self, view_id: str) -> discord.ui.View | None:
        return self.views.get(view_id)

view_registry = ViewRegistry()