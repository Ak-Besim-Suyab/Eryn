import discord
from discord import ui

from data import CONTAINERS, RESOURCES
from lib import container, resource
from lib.entity import building

from models import Building

class SanctuaryView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout = None)
        self.name = "sanctuary"
        self.data = CONTAINERS.get(self.name)
        self.render()

    def render(self):

        build: Building
        build, _ = Building.get_or_create(id=self.name)

        contributions = building.get_contributions(self.name)

        kwargs = {"level": build.level}

        for res, current in contributions.items():
            level = 1
            required = 0
            while True:
                required += building.get_required_resources(level=level)
                if required >= current:
                    break
                level += 1

            kwargs[f"level_{res}"] = level
            kwargs[f"current_{res}"] = current
            kwargs[f"required_{res}"] = required
            
        action_row = ui.ActionRow()
        action_row.add_item(SanctuaryOption())

        con = container.build(self.data, **contributions, **kwargs)
        con.add_item(action_row)

        self.clear_items()
        self.add_item(con)

class SanctuaryOption(ui.Select):
    def __init__(self):

        actions = {
            ("木材（消耗：100 木材）", "wood:100"),
            ("石材（消耗：100 石材）", "stone:100"),
            ("食物（消耗：100 食物）", "food:100"),
            ("木材（消耗：1000 木材）", "wood:1000"),
            ("石材（消耗：1000 石材）", "stone:1000"),
            ("食物（消耗：1000 食物）", "food:1000"),
        }

        options = []
        for label, value in actions:
            options.append(discord.SelectOption(label = label, value = value))

        super().__init__(
            placeholder = "選擇提供項目（可複選）", 
            min_values = 1,
            max_values = len(actions),
            options = options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)
 
        for value in self.values:
            res, quantity = value.split(":")
            success, msg = building.add_contribution(interaction.user.id, "sanctuary", res, int(quantity))

        view = self.view; view.render()
        await interaction.edit_original_response(view=view)