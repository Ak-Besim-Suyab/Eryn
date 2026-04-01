import discord

from models.player import Player
from models.region import region_manager
from models.resource import resource_manager

class ActionOption(discord.ui.Select):
    def __init__(self):

        self.actions = [
            {
                "label": "採集",
                "description": "前往附近的地點採集資源",
                "emoji": "🌿",
                "value": "garden",
                "function": self.garden
            }
        ]

        options = []

        for action in self.actions:
            option = discord.SelectOption(
                label=action["label"], 
                value=action["value"], 
                description=action["description"], 
                emoji=action["emoji"]
            )
            options.append(option)

        super().__init__(
            placeholder="選擇行動", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]

        for action in self.actions:
            if action["value"] == selected_value:
                await action["function"](interaction)
                break

    async def garden(self, interaction: discord.Interaction):
        pass