import discord

from datetime import datetime
from database.player import Player

from cores.logger import logger

class LevelSession:
    def __init__(self, bot):
        self.bot = bot
        self.message_cooldown = 30
        self.message_exp = 5
        self.message_cooldowns = {}
        self.timestamps = {} # 用於追蹤用戶的最後操作時間戳    

    def settle_message_experience(self, message: discord.Message):
        # 忽略私人訊息
        if not message.guild:
            return
        
        user_id = message.author.id
        now = datetime.now().timestamp()
        
        # 檢查冷卻時間
        if user_id in self.message_cooldowns:
            if now - self.message_cooldowns[user_id] < self.message_cooldown:
                return
        
        # 更新冷卻時間戳
        self.message_cooldowns[user_id] = now

        # 增加經驗值
        player = Player.get_or_create_player(message.author.id, message.author.display_name)
        player.add_experience(self.message_exp)

        logger.info(f"已為 {message.author} 結算自訊息獲得的角色經驗，總共獲得: {self.message_exp}")

    def settle_voice_experience(self, member: discord.Member):
        now = datetime.now().timestamp()

        if member.id not in self.timestamps:
            logger.warning(f"找不到 {member} 的時間戳記，無法進行結算。")
            return
        
        timestamp = self.timestamps[member.id]
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
        player = Player.get_or_create_player(member.id, member.display_name)
        player.add_experience(total_experience)

        logger.info(f"已為 {member} 結算自語音計時獲得的角色經驗，總共獲得: {total_experience}")


    def save_timestamp(self, member: discord.Member):
        self.timestamps[member.id] = datetime.now().timestamp()
        logger.debug(f"[LevelSession] 成功保存 {member} 的時間戳記")

    def remove_timestamp(self, member: discord.Member):
        if member.id in self.timestamps:
            del self.timestamps[member.id]
            logger.debug(f"[LevelSession] 成功移除 {member} 的時間戳記")