import discord
from discord import ui
from discord.ext import commands

from data import CONTAINERS, REGIONS

from lib import container, player, region, role, view
from lib.system import turn

from ui.button import CHARACTER_BUTTON, MAP_GUIDE_BUTTON


class WorldMapCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def world_map(self, ctx: commands.Context):
        await ctx.send(view=WorldMapView())


class WorldMapView(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        _select = ui.ActionRow(WorldMapSelect())
        _container = (
            container
            .build(CONTAINERS.get("world_map"))
            .add_item(_select)
        )

        self.add_item(_container)
        self.add_item(ui.ActionRow(CHARACTER_BUTTON, MAP_GUIDE_BUTTON))


class WorldMapConfirmView(discord.ui.LayoutView):
    def __init__(self, user: discord.abc.User, destination: str):
        super().__init__(timeout=None)

        self.user = user
        self.destination = REGIONS.get(destination)

        current_region = REGIONS.get(player.get_region(user.id))

        self.cost = region.get_cost(current_region.id, self.destination.id)

        confirm_button = ui.Button(
            label="確定",
            style=discord.ButtonStyle.secondary,
            custom_id="world_map:confirm",
        )
        confirm_button.callback = self.confirm_button

        cont = ui.Container()
        cont.add_item(ui.TextDisplay(content=f"## {user.display_name}"))
        cont.add_item(
            ui.Section(
                f"從{current_region.name}前往{self.destination.name}將會累積 **{self.cost}** 回合，確定要前往嗎？",
                accessory=confirm_button,
            )
        )

        self.add_item(cont)

    async def confirm_button(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        success, _ = region.move(interaction.user.id, self.destination.id)

        if success:
            turn.add(interaction.user.id, self.cost)

            if isinstance(interaction.user, discord.Member) and self.destination.role_id is not None:
                region_role_ids = [
                    r.role_id for r in REGIONS.get_all() if r.role_id is not None
                ]
                await role.switch(
                    interaction.user,
                    self.destination.role_id,
                    region_role_ids,
                    reason=f"移動至地區：{self.destination.name}",
                )

        c = discord.ui.Container()
        c.add_item(ui.TextDisplay(content=f"經過一段時間的跋涉後，你成功到達{self.destination.name}。"))

        v = discord.ui.LayoutView()
        v.add_item(c)

        await interaction.followup.send(view=v, ephemeral=True)


class WorldMapSelect(ui.Select):
    def __init__(self):

        # 選項列表, 修改列表請調整此參數
        regions = ["port_norse", "boreal_forest", "mine"]

        options = []
        for reg_id in regions:
            reg = REGIONS.get(reg_id)
            options.append(
                discord.SelectOption(
                    label=reg.name,
                    description=reg.description,
                    value=reg.id,
                )
            )

        super().__init__(
            placeholder="選擇要前往的地區",
            options=options,
            custom_id="world_map:select",
        )

    async def callback(self, interaction: discord.Interaction):

        current = REGIONS.get(player.get_region(interaction.user.id))

        if current.id == self.values[0]:
            load = {
                "player_name": interaction.user.display_name,
                "region_name": current.name,
            }
            await interaction.response.send_message(view=view.create("map_choose_fail", **load), ephemeral=True)
            return

        await interaction.response.send_message(
            view=WorldMapConfirmView(interaction.user, self.values[0]),
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(WorldMapCog(bot))
