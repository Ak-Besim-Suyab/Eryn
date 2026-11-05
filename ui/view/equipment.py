import discord
from discord import ui

from data import RACES
from data.schema import Item

from lib import player

class EquipmentView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, item: Item = None):
        super().__init__(timeout = None)
        self.user = user
        self.item = item
        self.render()


    def render(self):
        action_row = ui.ActionRow()
        action_row.add_item(EquipmentSelect(self.user, self.item))

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name} 裝備"))
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(action_row)

        self.clear_items()
        self.add_item(container)

class EquipmentSelect(ui.Select):
    def __init__(self, user: discord.abc.User, item: Item):
        self.user = user
        self.item = item

        race = RACES.get(player.get_race(self.user.id))

        options = []
        for slot in race.equip_slots:

            key, sep, value = slot.partition(":")

            options.append(discord.SelectOption(
                label = key,
                value = slot
            ))

        super().__init__(
            placeholder = "要裝備在哪？",
            min_values = 1,
            max_values = 1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{self.values[0]}", ephemeral=True)