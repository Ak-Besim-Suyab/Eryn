import random
from discord.ext import commands, tasks

from cores import database
from cores import logger

from lib import resource

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
        pool = ["wood", "stone", "food"]

        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:
                if member.bot:
                    continue

                res = random.choices(pool, weights=[100, 100, 100])[0]
                rewards.append((member, res))

        try:
            with database.atomic():
                for member, res in rewards:
                    resource.give(member, res, 1)

        except Exception as e:
            logger.exception(f"語音獎勵發放失敗：{e}")

    @loop.before_loop
    async def loop_wait(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(LoopCog(bot))