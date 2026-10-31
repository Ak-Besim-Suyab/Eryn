import discord
from discord import ui

from data import registry
from lib.builder import build_container
from lib import resource, building

class SanctuaryView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout = None)

        self.data = registry.container.get("sanctuary")
        self.render()

    def render(self):

        contributions = building.get_building_contributions("sanctuary")

        action_row = ui.ActionRow()
        action_row.add_item(SanctuaryOption())

        container = build_container(self.data, **contributions)
        container.add_item(action_row)

        self.clear_items()
        self.add_item(container)

class SanctuaryOption(ui.Select):
    def __init__(self):

        data = {
            ("木材（消耗：100 木材）", "wood"),
            ("石材（消耗：100 石材）", "stone"),
            ("食物（消耗：100 食物）", "food"),
        }

        options = []
        for label, value in data:
            options.append(discord.SelectOption(label = label, value = value))

        super().__init__(
            placeholder = "選擇要提供的項目（可複選）", 
            min_values = 1,
            max_values = len(data),
            options = options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral = True)
 
        lines = ["已捐助資源："]
        for value in self.values:
            res = registry.resource.get(value)
            success = resource.remove(interaction.user.id, value, 100)
            if not success:
                continue

            building.add_contribution(interaction.user.id, "sanctuary", value, 100)

            lines.append(f"- {res.icon}{res.name}")

        view: SanctuaryView
        view = self.view
        
        view.render()

        await interaction.edit_original_response(view=view)
        await interaction.followup.send("\n".join(lines))