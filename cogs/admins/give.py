import discord
from discord.ext import commands

from lib import item

"""
此元件用於管理物品給予或移除的指令
"""

class GiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx: commands.Context, member: discord.Member, item_id: str, amount: int=1):
        
        quantity = item.give(member.id, item_id, amount)

        await ctx.send(f"✅ 已給予 {member.name} {amount} 個 {item_id}")

        
async def setup(bot: commands.Bot):
    await bot.add_cog(GiveCog(bot))