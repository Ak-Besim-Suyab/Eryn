import discord
from discord.ext import commands
from discord import app_commands

from data import CONTAINERS

import ui

from lib import view
from lib import container
from lib.util.ansi import ANSI, wrap_ansi

class UnitTestCog(commands.Cog):
    """ 
    這個 Cog 用於需要線上運作的單元測試 (例如: 互動元件) 普通單元測試請使用 scripts
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def line(self, ctx: commands.Context):

        content = "您目前位於**避風港**，選擇前往**北方森林**將會累積 **12** 回合，確定要前往嗎？"

        c = discord.ui.Container()
        c.add_item(discord.ui.TextDisplay(content=f"### {ctx.author.display_name}"))
        c.add_item(discord.ui.TextDisplay(content=content))

        v = discord.ui.LayoutView()
        v.add_item(c)

        await ctx.send(view=v)


    @commands.command()
    @commands.is_owner()
    async def ansi(self, ctx: commands.Context):
        text = ANSI("你獲得 50 經驗值").gold()
        ansi_text = wrap_ansi(str(text))

        await ctx.send(ansi_text)

        container = (discord.ui.Container()
                     .add_item(discord.ui.TextDisplay(content = ansi_text)))

        view = (discord.ui.LayoutView(timeout = None)
                .add_item(container))
        
        await ctx.send(view = view)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        con = container.build(CONTAINERS.get("world_map"))

        con.add_item(
            discord.ui.ActionRow()
            .add_item(ui.RegionSelect())
        )

        view = discord.ui.LayoutView(timeout = None).add_item(con)

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
