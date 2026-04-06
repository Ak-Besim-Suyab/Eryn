import os
import discord
from peewee import SqliteDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "generic.db")

db = SqliteDatabase(DB_PATH)

TH_HAVEN = 1190027756482859038
AK_BESIM = 1193049715638538280

GUILD_TH_HAVEN = discord.Object(id=TH_HAVEN)
GUILD_AK_BESIM = discord.Object(id=AK_BESIM)

ADMIN_BOOLEAN = True

ANNOUNCEMENT_CHANNEL = {
    TH_HAVEN: 1198867692497674241,
    AK_BESIM: 1423681593402462208
}