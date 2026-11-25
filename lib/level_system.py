"""
這個模組用來處理玩家在伺服器活動時的經驗值加成計算與語音經驗結算
"""

import discord

from datetime import datetime

from models import Statistic

from cores.logger import logger
from lib import building, player

voice_experience = 1

def get_sanctuary_bonus(resource_name: str, per_level: float) -> float:
    """
    依據聖所的等級計算經驗加成倍率, 公式為 (1 + 材料等級 * 每材料等級加成) * (1 + 聖所等級 * 0.01)

    b_level: 聖所等級, 增加更多經驗值 (外部乘算)
    m_level: 聖所材料等級, 增加額外經驗值 (內部加算)
    """
    b_level = building.get_level("sanctuary")
    m_level = building.get_rlevel("sanctuary", resource_name)
    return (1 + max(0, m_level) * per_level) * (1 + max(0, b_level) * 0.01)

def give_voice_experience(member: discord.Member):

    # 取得現在的時間
    now = datetime.now().timestamp()

    # 取得玩家最後加入語音的時間
    timestamp = player.get_timestamp_voice(member.id)
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

    bonus = get_sanctuary_bonus("stone", 0.01)
    total_experience = round(elapsed_minutes * voice_experience * bonus, 2)
    player.add_experience(member.id, total_experience)

    stats = Statistic.get_or_create_stat(member.id)
    stats.total_voice += elapsed_minutes
    stats.save()

    logger.debug(f"給予 {member.display_name} 語音經驗值: {total_experience} exp (倍率: {bonus:.2f}x), 累積時間: {elapsed_minutes:.2f} 分鐘")

def save_timestamp(member: discord.Member):
    player.set_timestamp_voice(member.id, datetime.now().timestamp())

def remove_timestamp(member: discord.Member):
    player.set_timestamp_voice(member.id, None)
