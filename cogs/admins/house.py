import discord
from discord.ext import commands
from pathlib import Path

from cores import asset
from cores.logger import logger

from systems import house

class AdminHouseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 宣告指令群組 house
    # =========================
    @commands.group()
    @commands.is_owner()
    async def house(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("使用 !house + 子指令呼叫對應方法")


    @house.command(name="register")
    @commands.is_owner()
    async def register(self, ctx: commands.Context, channel: discord.VoiceChannel, member: discord.Member):

        """這是社群專用指令，為頻道登記持有者，使用時須要提供「頻道」與「成員」相關參數"""

        if not isinstance(channel, discord.VoiceChannel):
            await ctx.send("提供的頻道似乎不是小屋，請確認頻道類型是否正確")
            return 

        registered_house, created = house.register(channel.id, member.id)

        if not created:
            fail_message = f"⚠️ {channel.name} 已登記在 {registered_house.owner.display_name} 名下，無法再次登記。"
            await ctx.send(fail_message), logger.info(fail_message)
            return

        success_message = f"✅ 成功將 {channel.name} 登記在 {member.display_name} 名下。"
        await ctx.send(success_message), logger.info(success_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminHouseCog(bot))