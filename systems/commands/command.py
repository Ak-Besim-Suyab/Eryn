"""
這是指令 (技能) 的抽象類別
目前定義冷卻時間與使用者的時間戳記，以及判斷冷卻的方法
"""
import discord
import time
from functools import wraps

class Command:
    def __init__(self, skill_cooldown: float = 5.0):
        self.skill_cooldown = skill_cooldown
        self.skill_timestamps = {}

    def is_cooldown(func):
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            now = time.time()
            if interaction.user.id in self.skill_timestamps:
                elapsed = now - self.skill_timestamps[interaction.user.id]
                if elapsed < self.skill_cooldown:
                    remaining = self.skill_cooldown - elapsed
                    await interaction.response.send_message(f"❌ 技能冷卻中，請等待 {remaining:.1f} 秒後再試。", ephemeral=True)
                    return
                
            self.skill_timestamps[interaction.user.id] = now
            return await func(self, interaction, *args, **kwargs)
            
        return wrapper