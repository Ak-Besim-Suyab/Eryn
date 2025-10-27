import discord
from discord.ext import commands
from discord import app_commands

import asyncio

from player_manager import player_manager

GUILD_TH_HAVEN = discord.Object(id=1193049715638538280)
GUILD_AK_BESIM = discord.Object(id=1190027756482859038)

class Combat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('[Command] Combat command initialized successfully.')

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="combat", description="尋找強敵並進行戰鬥")
    async def combat(self, interaction: discord.Interaction):
        pass

async def setup(bot):
    await bot.add_cog(Combat(bot))

# 發現目標：
# 史萊姆 Lv.1
# 野狼 Lv.2
# 村民 Lv.3
# 守衛 Lv.10
# ooo的綿羊 Lv.1

# 你想對誰發起攻擊？