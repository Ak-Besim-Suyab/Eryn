import discord

# from systems.actions.garden import garden_skill

class ActionOption(discord.ui.Select):
    def __init__(self):

        self.actions = [
            {
                "label": "採集",
                "description": "前往附近的地點採集資源",
                "emoji": "🌿",
                "value": "garden",
                "function": None
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
        
        await interaction.response.edit_message(view=self.view) #重置選項

        selected_value = self.values[0]
        for action in self.actions:
            if action["value"] == selected_value:
                await action["function"](interaction)
                break