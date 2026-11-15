import discord
from discord.ext import commands

from lib import item
from lib import resource

"""
此元件用於管理物品給予或移除的指令
"""

class GiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx: commands.Context, member: discord.Member, item_id: str, amount: int=1):
        
        success = item.give(member.id, item_id, amount)

        if not success:
            await ctx.send(f"❌ 給予 {member.name} {amount} 個 {item_id} 失敗")
            return

        await ctx.send(f"✅ 已給予 {member.name} {amount} 個 {item_id}")

    @commands.command()
    @commands.is_owner()
    async def give_res(self, ctx: commands.Context, member: discord.Member, rid: str, amount: int):

        if not amount:
            await ctx.send("❌ 請輸入數量")
            return
        
        success = resource.give(member.id, rid, amount)

        if not success:
            await ctx.send(f"❌ 給予 {member.name} {amount} 個 {rid} 失敗")
            return

        await ctx.send(f"✅ 已給予 {member.name} {amount} 個 {rid}")

        
async def setup(bot: commands.Bot):
    await bot.add_cog(GiveCog(bot))