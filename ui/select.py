import discord

class LookSelect(discord.ui.Select):
    def __init__(self, state: object, entries: list[dict]):
        self.state = state
        self.entries = entries

        options = [
            discord.SelectOption(
                label=entry.get("entity_name"), 
                value=entry.get("entity_id"), 
                emoji="❓"
            ) 
            for entry in entries
        ]

        super().__init__(
            placeholder = "請選擇", 
            options = options, 
            min_values = 1, 
            max_values = 1
        )

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        for entry in self.entries:
            if entry.get("entity_id") == choice:
                await self.state.select_entry(interaction, entry)