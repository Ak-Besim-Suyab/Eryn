import discord
from discord.ext import commands

import data

"""此元件用於管理物品給予或移除的指令
"""

class GiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx: commands.Context, member: discord.Member, item_name: str, amount: int = 1):
        pass
        
async def setup(bot: commands.Bot):
    await bot.add_cog(GiveCog(bot))