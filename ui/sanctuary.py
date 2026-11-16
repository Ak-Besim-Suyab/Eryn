import discord
from discord import ui

from data import CONTAINERS, LINES
from lib import container
from lib.entity import building
from lib import view
from lib import skill

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

        kwargs = {
            "level": build.level
        }

        for res, current in contributions.items():

            rlevel = building.get_rlevel(self.name, res)

            kwargs[f"level_{res}"] = rlevel
            kwargs[f"current_{res}"] = current
            kwargs[f"required_{res}"] = building.get_reqrsc(level=rlevel)

            match res:
                case "food":
                    kwargs[f"effect_{res}"] = rlevel * 2
                case "wood":
                    kwargs[f"effect_{res}"] = rlevel * 2
                case "stone":
                    kwargs[f"effect_{res}"] = rlevel * 1.5
                case "iron":
                    kwargs[f"effect_{res}"] = rlevel * 1
            
        action_row = ui.ActionRow()
        action_row.add_item(SanctuaryOption())

        con = container.build(self.data, **contributions, **kwargs)
        con.add_item(action_row)

        self.clear_items()
        self.add_item(con)

class SanctuaryOption(ui.Select):
    def __init__(self):

        actions = [
            ("🥩提供 100 份食物",   "food:100"),
            ("🥩提供 500 份食物",   "food:500"),
            ("🥩提供 1,000 份食物", "food:1000"),

            ("🪵提供 100 份木材",   "wood:100"),
            ("🪵提供 500 份木材",   "wood:500"),
            ("🪵提供 1,000 份木材", "wood:1000"),

            ("🪨提供 100 份石材",   "stone:100"),
            ("🪨提供 500 份石材",   "stone:500"),
            ("🪨提供 1,000 份石材", "stone:1000"),

            ("🪨提供 100 份鐵",   "iron:100"),
            ("🪨提供 500 份鐵",   "iron:500"),
            ("🪨提供 1,000 份鐵", "iron:1000"),
        ]

        options = []
        for label, value in actions:
            options.append(discord.SelectOption(label = label, value = value))

        super().__init__(
            placeholder = "選擇提供項目", 
            options = options,
            custom_id = "sanctuary:select",
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)
 
        res, quantity = self.values[0].split(":")
        success, msg = building.add_contribution(interaction.user.id, "sanctuary", res, int(quantity))

        if success:
            building.add_experience("sanctuary", float(quantity))
            skill.add_experience(interaction.user.id, "faith", float(quantity))

            v = self.view; v.render()
            await interaction.edit_original_response(view=v)

        if not success and msg:
            kwargs = {
                "player_name": interaction.user.display_name,
                "line": LINES.get("offer_fail").random(),
            }

            v = view.create("offer_fail", **kwargs)

            await interaction.followup.send(view=v, ephemeral=True)