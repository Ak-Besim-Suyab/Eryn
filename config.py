import re
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

# 骰子
DICE_PATTERN = re.compile(r"^\s*(\d{1,2})?[dD](\d{1,4})\s*$")
MAX_SIDES = 100

OMIKUJI_POOL = [
    "<:dai_kichi:1561975565500817428>",
    "<:kichi:1561975597335314542>",
    "<:sho_kichi:1561975608949481542>",
    "<:sho_kyo:1561975734153781318>",
    "<:kyo:1561975744417239050>",
    "<:dai_kyo:1561975786398023780>",
]

SIGN_POOL = [
    "<:rock:1563601501442543688>", 
    "<:paper:1563601513413087305>", 
    "<:scissors:1563601489606222005>"
]