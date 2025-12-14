import discord
import random
from discord.ext import commands

class TestEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test_embed")
    async def test_embed(self, ctx: commands.Context):

        await ctx.send("")

async def setup(bot):
    await bot.add_cog(TestEmbed(bot))