from discord.ext import commands
from discord import ui

from data import container_data
from lib import builder

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def announce(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("請使用 !announce + 子指令呼叫方法", ephemeral=True)

    @announce.command(name="template")
    @commands.is_owner()
    async def template(self, ctx: commands.Context):
        view = ui.LayoutView().add_item(builder.build_container(container_data.get("template")))
        await ctx.send(view = view)

    @announce.command(name="travel_guide")
    @commands.is_owner()
    async def travel_guide(self, ctx: commands.Context):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))