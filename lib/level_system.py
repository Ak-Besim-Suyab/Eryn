"""
這個類別用來處理玩家在伺服器活動時能獲得的經驗管道
目前能獲得經驗的管道有：
- 發送訊息 / message experience
- 給予反應 / reaction experience
- 加入/離開語音 / voice experience
"""

import discord
import config
import player

from datetime import datetime

from models import Player
from models import Statistic

from cores.logger import logger

player_message_cooldowns = {}
player_reaction_cooldowns = {}

message_experience = 5
reaction_experience = 5

def give_message_experience(member: discord.Member):
    """
    注意事項：這裡傳入的物件是 message.author 需要確保物件本身指向 discord.Member 否則會報錯
    """
    user_id = member.id
    now = datetime.now().timestamp()
    
    # 檢查冷卻時間
    if user_id in player_message_cooldowns:
        if now - player_message_cooldowns[user_id] < config.MESSAGE_COOLDOWN:
            return
    
    # 更新冷卻時間戳
    player_message_cooldowns[user_id] = now

    Player.add_experience(user_id, message_experience)

    logger.debug(f"給予 {member.display_name} 訊息經驗值: {message_experience} exp")

def give_reaction_experience(member: discord.Member):
    
    user_id = member.id
    now = datetime.now().timestamp()

    # 檢查冷卻時間
    if user_id in player_reaction_cooldowns:
        if now - player_reaction_cooldowns[user_id] < config.REACTION_COOLDOWN:
            return
    
    # 更新冷卻時間戳
    player_reaction_cooldowns[user_id] = now

    Player.add_experience(user_id, reaction_experience)

    logger.debug(f"給予 {member.display_name} 反應經驗值: {reaction_experience} exp")

def give_voice_experience(member: discord.Member):

    # 取得現在的時間
    now = datetime.now().timestamp()

    # 取得玩家最後加入語音的時間
    timestamp = Player.get_timestamp_voice(member.id)
    if timestamp is None:
        logger.warning(f"{member.display_name} 沒有語音時間戳記，無法進行結算。")
        return

    # 計算待在語音的時間
    elapsed_minutes = (now - timestamp) / 60

    # 獎勵機制
    # 根據待在語音的時間給予不同的經驗值，在 2 小時後有最大值
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

    stats = Statistic.get_or_create_stat(member.id)
    stats.total_voice_time += elapsed_minutes
    stats.save()

    logger.info(f"給予 {member.display_name} 語音經驗值: {total_experience} exp, 累積時間: {elapsed_minutes:.2f} 分鐘")

def save_timestamp(member: discord.Member):
    Player.save_timestamp_voice(member.id)
    logger.info(f"成功保存 {member} 的時間戳記")

def remove_timestamp(member: discord.Member):
    Player.remove_timestamp_voice(member.id)
    logger.info(f"成功移除 {member} 的時間戳記")
