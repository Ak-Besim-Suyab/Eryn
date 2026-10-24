import discord
from discord.ext import commands

import data
from lib import player

"""此元件用於管理物品給予或移除的指令
"""

class GiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def give(self, ctx: commands.Context, member: discord.Member, item_name: str, amount: int = 1):
        
        item = data.item.get(item_name)
        if item is None:
            await ctx.send("❌ 錯誤，物品不存在")
            return
        if amount <= 0:
            await ctx.send("❌ 錯誤，數量必須大於 0")
            return

        quantity = player.give_item(member.id, item.id, amount)

        await ctx.send(f"✅ 已給予 {member.name} {amount} 個 {item.name} ({quantity} 個)")

        
async def setup(bot: commands.Bot):
    await bot.add_cog(GiveCog(bot))