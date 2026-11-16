import random
from discord.ext import commands, tasks

from data import LOOT_TABLES

from cores import database
from cores import logger

from lib import resource
from lib import player

from config import TH_HAVEN

class LoopCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(minutes=1)
    async def loop(self):
        guild = self.bot.get_guild(TH_HAVEN)

        rewards = []

        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:

                # 忽略機器人
                if member.bot:
                    continue

                # 取得戰利品表
                loot_table = LOOT_TABLES.get(player.get_region(member.id))
                if not loot_table:
                    continue

                rewards.append((member, loot_table.roll(1)))

        try:
            with database.atomic():
                for member, roll in rewards:
                    for (item_type, item_id), quantity in roll.items():
                        resource.give(member.id, item_id, quantity)

        except Exception as e:
            logger.exception(f"語音獎勵發放失敗：{e}")

    @loop.before_loop
    async def loop_wait(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(LoopCog(bot))