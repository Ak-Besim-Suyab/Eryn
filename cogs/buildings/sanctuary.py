import discord
from discord.ext import commands
from discord import ui

from data import CONTAINERS, MATERIALS
from data.enums import BuildingName

from ui.button import BUILDING_GUIDE_BUTTON, RESOURCE_BUTTON
from lib.entity import building
from lib import view, skill, container

class SanctuaryCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def sanctuary(self, ctx: commands.Context):
        await ctx.send(view=SanctuaryView())

class SanctuaryView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout = None)
        self.name = BuildingName.SANCTUARY
        self.render()

    def render(self):
        b         = building.get(self.name)
        contributions = building.get_contributions(self.name)

        build_level = b.level

        kwargs: dict = {
            "level": build_level
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
        action_row.add_item(SanctuarySelect())

        con = container.build(CONTAINERS.get(self.name), **contributions, **kwargs)
        con.add_item(action_row)

        self.clear_items()
        self.add_item(con)
        self.add_item(ui.ActionRow(RESOURCE_BUTTON, BUILDING_GUIDE_BUTTON))

class SanctuarySelect(ui.Select):
    def __init__(self):

        actions = [
            ("提供 100 食物",   "food:100",  "🥩"),
            ("提供 500 食物",   "food:500",  "🥩"),
            ("提供 1,000 食物", "food:1000", "🥩"),

            ("提供 100 木材",   "wood:100",  "🪵"),
            ("提供 500 木材",   "wood:500",  "🪵"),
            ("提供 1,000 木材", "wood:1000", "🪵"),

            ("提供 100 石材",   "stone:100",  "🪨"),
            ("提供 500 石材",   "stone:500",  "🪨"),
            ("提供 1,000 石材", "stone:1000", "🪨"),

            ("提供 100 鐵",   "iron:100",  "<:iron:1573435315522248725>"),
            ("提供 500 鐵",   "iron:500",  "<:iron:1573435315522248725>"),
            ("提供 1,000 鐵", "iron:1000", "<:iron:1573435315522248725>"),
        ]

        options = []
        for label, value, emoji in actions:
            options.append(discord.SelectOption(label = label, value = value, emoji = emoji))

        super().__init__(
            placeholder = "選擇要提供的材料", 
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

async def setup(bot: commands.Bot):
    await bot.add_cog(SanctuaryCog(bot))