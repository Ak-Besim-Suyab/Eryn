from discord.ext import commands

from game import guide

from cores import logger

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def announce(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("請使用 !announce + 子指令呼叫對應方法")

    @announce.command(name="tavern")
    @commands.is_owner()
    async def tavern(self, ctx: commands.Context):
        """這個指令用於發布在小酒館的置頂公告"""
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))