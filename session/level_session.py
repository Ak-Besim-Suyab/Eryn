import discord

from datetime import datetime
from database.character import Character

class LevelSession:
    def __init__(self, bot):
        self.bot = bot
        self.message_cooldown = 30
        self.message_exp = 5
        self.message_cooldowns = {}

    def message_xp(self, message: discord.Message):
        if message.author.bot:
            return
        
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
        result = Character.add_experience(user_id, self.message_exp)
        
        # 如果升級了，發送升級通知
        if result['leveled_up']:
            self.bot.dispatch("leveling", message.author, "釣魚", result.get('level'))