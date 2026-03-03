import discord
from discord.ext import commands

from session.level_session import LevelSession

from cores.logger import logger

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = LevelSession(bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 忽略機器人訊息
        if message.author.bot:
            return
        
        self.session.give_message_experience(message)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        # 忽略機器人
        if member.bot:
            return
        
        # 語音狀態檢查
        if after.channel and not before.channel:
            logger.debug(f"[語音] {member.display_name} 加入語音頻道：{after.channel.name}")
            self.session.save_timestamp(member)

        elif before.channel and not after.channel:
            logger.debug(f"[語音] {member.display_name} 離開語音頻道：{before.channel.name}")
            self.session.give_voice_experience(member)
            self.session.remove_timestamp(member)


async def setup(bot):
    await bot.add_cog(Leveling(bot))
