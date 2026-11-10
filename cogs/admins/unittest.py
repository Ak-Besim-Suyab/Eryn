import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

from data import CONTAINERS

from lib import view
from lib.builder import build_container
from ui.select.region import RegionSelect

class UnitTestCog(commands.Cog):
    """ 這個 Cog 用於需要傳入互動元件的單元測試, 普通單元測試請到 scripts 進行編寫
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        container = build_container(CONTAINERS.get("world_map"))
        container.add_item(ui.ActionRow().add_item(RegionSelect()))
        view = ui.LayoutView(timeout = None).add_item(container)
        await ctx.send(view = view)

    @app_commands.command(name="測試", description="測試用指令")
    @app_commands.default_permissions(administrator=True)
    async def unittest_slash(self, interaction: discord.Interaction):

        await interaction.response.send_message(view=view.create("sanctuary"))

        # # test if create_view function works.
        # view = create_view("template")
        # await interaction.response.send_message(view=view)

        # # create fake param dict.
        # param = {
        #     "name": "Elin",
        #     "level": 1,
        #     "experience": 100
        # }

        # # test if function works with container object, string and param 
        # container = ui.Container()
        # container.add_item(ui.TextDisplay(content = "# This is Another Container Test."))
        # view = create_view(container, "template_param", **param)
        # await interaction.followup.send(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnitTestCog(bot))
