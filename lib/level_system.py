"""
這個類別用來處理玩家在伺服器活動時能獲得的經驗管道
目前能獲得經驗的管道有：
- 發送訊息 / message experience
- 給予反應 / reaction experience
- 加入/離開語音 / voice experience
"""

import discord
import config

from datetime import datetime

from models import Player
from models import Statistic

from cores.logger import logger
from lib import building

player_message_cooldowns = {}
player_reaction_cooldowns = {}

message_experience = 5
reaction_experience = 5
voice_experience = 1

def _get_sanctuary_bonus(resource_name: str, per_level: float) -> float:
    """
    依據聖所指定材料的等級計算經驗加成倍率（等級 1 為 1.0，每升 1 級增加 per_level）
    """
    level = building.get_rlevel("sanctuary", resource_name)
    return 1 + max(0, level - 1) * per_level

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

    bonus = _get_sanctuary_bonus("food", 0.02)
    total_experience = round(message_experience * bonus, 2)
    Player.add_experience(user_id, total_experience)

    logger.debug(f"給予 {member.display_name} 訊息經驗值: {total_experience} exp (倍率: {bonus:.2f}x)")

def give_reaction_experience(member: discord.Member):
    
    user_id = member.id
    now = datetime.now().timestamp()

    # 檢查冷卻時間
    if user_id in player_reaction_cooldowns:
        if now - player_reaction_cooldowns[user_id] < config.REACTION_COOLDOWN:
            return
    
    # 更新冷卻時間戳
    player_reaction_cooldowns[user_id] = now

    bonus = _get_sanctuary_bonus("wood", 0.02)
    total_experience = round(reaction_experience * bonus, 2)
    Player.add_experience(user_id, total_experience)

    logger.debug(f"給予 {member.display_name} 反應經驗值: {total_experience} exp (倍率: {bonus:.2f}x)")

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

    # 暫時移除 2 小時有最大值的時長分段倍率設定，先固定以每分鐘基礎經驗結算
    # match elapsed_minutes:
    #     case minutes if minutes > 0 and minutes <= 60:
    #         voice_experience = 1
    #     case minutes if minutes > 60 and minutes <= 120:
    #         voice_experience = 1.5
    #     case minutes if minutes > 120:
    #         voice_experience = 2

    bonus = _get_sanctuary_bonus("stone", 0.01)
    total_experience = round(elapsed_minutes * voice_experience * bonus, 2)
    Player.add_experience(member.id, total_experience)

    stats = Statistic.get_or_create_stat(member.id)
    stats.total_voice += elapsed_minutes
    stats.save()

    logger.debug(f"給予 {member.display_name} 語音經驗值: {total_experience} exp (倍率: {bonus:.2f}x), 累積時間: {elapsed_minutes:.2f} 分鐘")

def save_timestamp(member: discord.Member):
    Player.save_timestamp_voice(member.id)
    logger.debug(f"成功保存 {member} 的時間戳記")

def remove_timestamp(member: discord.Member):
    Player.remove_timestamp_voice(member.id)
    logger.debug(f"成功移除 {member} 的時間戳記")
