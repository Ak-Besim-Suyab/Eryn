import discord

class LookSelect(discord.ui.Select):
    def __init__(self, state: object, entry: list):
        self.state = state
        self.entry = entry
        super().__init__(placeholder = "請選擇", options = [], min_values = 1, max_values = 1)

    def set_option(self, data: list):
        options = [discord.SelectOption(label=e.get("entity_name"), value=e.get("entity_id"), emoji="❓") for e in self.entry]

        self.options = options

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        for e in self.entry:
            if e.get("entity_id") is choice:
                await self.state.on_target(e)