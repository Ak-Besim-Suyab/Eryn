import discord
from discord.ext import commands

from game.systems import LevelSystem
from cores.logger import logger

class VoiceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):

        # 忽略機器人進出語音
        if member.bot:
            return
        
        # 語音狀態檢查
        if after.channel and not before.channel:
            LevelSystem.save_timestamp(member)
            logger.debug(f"[語音] {member.display_name} 加入語音頻道：{after.channel.name}")
            
        elif before.channel and not after.channel:
            LevelSystem.give_voice_experience(member)
            LevelSystem.remove_timestamp(member)
            logger.debug(f"[語音] {member.display_name} 離開語音頻道：{before.channel.name}")

async def setup(bot):
    await bot.add_cog(VoiceListener(bot))