import discord
import json
from discord.ext import commands
from pathlib import Path

from cores.asset import AssetLoader
from cores.logger import logger

class AdminHouseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def house(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("使用 !house + 子指令呼叫對應方法")

    
    @house.command(name="check")
    @commands.is_owner()
    async def check(self, ctx: commands.Context):
        """
        驗證頻道是否有主人，主人指的是該頻道的擁有者
        資料會手動註冊頻道擁有者，這裡負責驗證哪些頻道屬於誰
        """
        # 獲取伺服器
        guild = ctx.guild

        # 逐個頻道檢查，如果該頻道已登記在資料中，印出匹配成功
        # 
        channel_leaved = []
        for channel in guild.channels:

            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                channel_leaved.append(channel.id)

                for member in guild.members:
                    path = Path(f"data/members/{member.id}.json")
                    if path.exists():
                        data = AssetLoader.load(f"data/members/{member.id}.json")
                        house = data.get("house")
                        if house and channel.id in house:
                            channel_leaved.remove(channel.id)
                            logger.info(f"找到匹配：成員 - {member.display_name} | 頻道 - {channel.name}")

        for channel in channel_leaved:
            logger.info(f"未找到匹配：頻道 - {guild.get_channel(channel).name}")
    
    @commands.command()
    @commands.is_owner()
    async def member_check(self, ctx: commands.Context):
        """
        驗證成員是否持有頻道
        """
        guild = ctx.guild

        member_leaved = []

        for member in guild.members:

            # 忽略機器人
            if member.bot:
                continue

            path = Path(f"data/members/{member.id}.json")

            if path.exists():

                data = AssetLoader.load(f"data/members/{member.id}.json")
                house = data.get("house")

                if house:
                    for channel in guild.channels:
                        if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                            if channel.id in house:
                                logger.info(f"找到小屋資料，成員 - {member.display_name} | 頻道 - {channel.name}")
                else:
                    member_leaved.append(member)

            else:
                logger.info(f"未找到成員資料，不進行小屋資料尋找，成員 - {member.display_name}")

        logger.info(f"以下成員未找到任何小屋資料：")
        for member in member_leaved:
            logger.info(f"成員 - {member.display_name} | 使用者名稱 - {member.name} | ID - {member.id}")


async def setup(bot):
    await bot.add_cog(AdminHouseCog(bot))