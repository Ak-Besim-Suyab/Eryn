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

        self.reaction_cooldown = 30
        self.reaction_exp = 5
        self.reaction_cooldowns = {}

    def give_message_experience(self, message: discord.Message):
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
        Player.add_experience(user_id, self.message_exp)

        logger.debug(f"給予 {message.author.display_name} 訊息經驗值: {self.message_exp} exp")

    def give_voice_experience(self, member: discord.Member):
        now = datetime.now().timestamp()

        timestamp = Player.get_timestamp_voice(member.id)

        if timestamp is None:
            logger.warning(f"{member.display_name} 沒有語音時間戳記，無法進行結算。")
            return
        
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
        Player.add_experience(member.id, total_experience)

        logger.info(f"給予 {member.display_name} 語音經驗值: {total_experience} exp, 累積時間: {elapsed_minutes:.2f} 分鐘")

    def give_reaction_experience(self, member: discord.Member):
        Player.add_experience(member.id, self.reaction_exp)

        logger.info(f"給予 {member.display_name} 反應經驗值： {self.reaction_exp} exp")

    def save_timestamp(self, member: discord.Member):
        now = datetime.now().timestamp()
        Player.save_timestamp_voice(member.id, now)
        logger.info(f"[LevelSession] 成功保存 {member} 的時間戳記")

    def remove_timestamp(self, member: discord.Member):
        Player.remove_timestamp_voice(member.id)
        logger.info(f"[LevelSession] 成功移除 {member} 的時間戳記")