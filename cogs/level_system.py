import discord
from discord.ext import commands

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_levelup(self, player):
        pass

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))