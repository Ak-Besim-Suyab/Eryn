from discord.ext import commands

from game import guide

from cores import logger
from cores.event import publish

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def announce(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("請使用 !announce + 子指令呼叫方法", ephemeral=True)

    @announce.command(name="manual")
    @commands.is_owner()
    async def manual(self, ctx: commands.Context):
        await publish("announce manual", ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))