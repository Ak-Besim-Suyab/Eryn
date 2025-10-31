import discord

class LookSelect(discord.ui.Select):
    def __init__(self, state: object, entries: list[dict]):
        self.state = state
        self.entries = entries

        options = [
            discord.SelectOption(
                label=entry.get("name"), 
                value=entry.get("uid"), 
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
            if entry.get("uid") == choice:
                await self.state.select_entry(interaction, entry)

class CombatSelect(discord.ui.Select):
    def __init__(self, state: object, entries: list[dict]):
        self.state = state
        self.entries = entries

        options = [
            discord.SelectOption(
                label=entry.get("action_name"), 
                value=entry.get("action_id"), 
                emoji="❓"
            ) 
            for entry in entries
        ]

        super().__init__(
            placeholder = "請選擇行動", 
            options = options, 
            min_values = 1, 
            max_values = 1
        )

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        if choice == "attack":
            await self.state.attack(choice)