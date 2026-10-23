import os
import discord

from zoneinfo import ZoneInfo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "generic.db")

TH_HAVEN = 1190027756482859038
GUILD_TH_HAVEN = discord.Object(id=TH_HAVEN)

timezone = ZoneInfo("Asia/Taipei")

# 常數
daily_experience = 50

# 冷卻時間
MESSAGE_COOLDOWN = 30
REACTION_COOLDOWN = 30