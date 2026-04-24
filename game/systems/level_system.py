"""
這個類別用來處理玩家在伺服器活動時能獲得的經驗管道
目前能獲得經驗的管道有：
- 發送訊息 / message experience
- 給予反應 / reaction experience
- 加入/離開語音 / voice experience
"""

import discord

from datetime import datetime

from game.model import Player

from cores.logger import logger

class LevelSystem:

    message_cooldown = 30
    message_experience = 5
    player_message_cooldowns = {}

    reaction_cooldown = 30
    reaction_experience = 5
    player_reaction_cooldowns = {}

    @classmethod
    def give_message_experience(cls, member: discord.Member):
        """
        注意事項：這裡傳入的物件是 message.author 需要確保物件本身指向 discord.Member 否則會報錯
        """
        user_id = member.id
        now = datetime.now().timestamp()
        
        # 檢查冷卻時間
        if user_id in cls.player_message_cooldowns:
            if now - cls.player_message_cooldowns[user_id] < cls.message_cooldown:
                return
        
        # 更新冷卻時間戳
        cls.player_message_cooldowns[user_id] = now

        Player.add_experience(user_id, cls.message_experience)

        logger.debug(f"給予 {member.display_name} 訊息經驗值: {cls.message_experience} exp")

    @classmethod
    def give_reaction_experience(cls, member: discord.Member):
        
        user_id = member.id
        now = datetime.now().timestamp()

        # 檢查冷卻時間
        if user_id in cls.player_reaction_cooldowns:
            if now - cls.player_reaction_cooldowns[user_id] < cls.reaction_cooldown:
                return
        
        # 更新冷卻時間戳
        cls.player_reaction_cooldowns[user_id] = now

        Player.add_experience(user_id, cls.reaction_experience)

        logger.debug(f"給予 {member.display_name} 反應經驗值: {cls.reaction_experience} exp")

    @classmethod
    def give_voice_experience(cls, member: discord.Member):
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

    @classmethod
    def save_timestamp(cls, member: discord.Member):
        Player.save_timestamp_voice(member.id)
        logger.info(f"[LevelSession] 成功保存 {member} 的時間戳記")

    @classmethod
    def remove_timestamp(cls, member: discord.Member):
        Player.remove_timestamp_voice(member.id)
        logger.info(f"[LevelSession] 成功移除 {member} 的時間戳記")
