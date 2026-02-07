import discord
from discord.ext import commands

from datetime import datetime

from utils.logger import logger

from database.character import Character
from session.level_session import LevelSession

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timestamps = {} # 用於追蹤用戶的最後操作時間戳
        self.level_session = LevelSession(bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        self.level_session.message_xp(message)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        if member.bot:
            return
        
        if after.channel and not before.channel:
            self.save_timestamp(member)
            logger.debug(f"[語音] {member} 加入語音頻道：{after.channel.name}")
        
        elif before.channel and not after.channel:
            self.settle(member)
            self.remove_timestamp(member)
            logger.debug(f"[語音] {member} 離開語音頻道：{before.channel.name}")

    def save_timestamp(self, member: discord.Member):
        self.timestamps[member] = datetime.now().timestamp()
        logger.debug(f"成功保存 {member} 的時間戳記")

    def remove_timestamp(self, member):
        if member in self.timestamps:
            del self.timestamps[member]
            logger.debug(f"已移除 {member} 的時間戳記")

    def settle(self, member: discord.Member):
        now = datetime.now().timestamp()

        if member not in self.timestamps:
            logger.warning(f"找不到 {member} 的時間戳記，無法進行結算。")
            return
        
        timestamp = self.timestamps[member]
        elapsed_minutes = (now - timestamp) / 60

        # 獎勵機制抽取，根據待在語音的時間給予不同的經驗值，在 2 小時後有最大值
        voice_experience = 0
        match elapsed_minutes:
            case minutes if minutes > 0 and minutes <= 60:
                voice_experience = 1
            case minutes if minutes > 60 and minutes <= 120:
                voice_experience = 1.5
            case minutes if minutes > 120:
                voice_experience = 2

        total_experience = int(elapsed_minutes * voice_experience)
        Character.add_experience(member.id, total_experience)

        logger.info(f"已為 {member} 結算角色經驗，獲得經驗: {total_experience}")


async def setup(bot):
    await bot.add_cog(Leveling(bot))
