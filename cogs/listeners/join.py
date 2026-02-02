import discord
from discord.ext import commands

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        # 忽略機器人加入事件
        if member.bot:
            return
        
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"咪！歡迎{member.mention}加入喵！")

async def setup(bot):
    await bot.add_cog(Join(bot))