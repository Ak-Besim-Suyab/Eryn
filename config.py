import discord
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    pass

TH_HAVEN = 1190027756482859038
AK_BESIM = 1193049715638538280

GUILD_TH_HAVEN = discord.Object(id=TH_HAVEN)
GUILD_AK_BESIM = discord.Object(id=AK_BESIM)

ADMIN_BOOLEAN = True

ANNOUNCEMENT_CHANNEL = {
    TH_HAVEN: 1198867692497674241,
    AK_BESIM: 1423681593402462208
}

daily_experience = 100
