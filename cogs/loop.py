import random
from discord.ext import commands, tasks

from cores import database
from cores import logger

from lib import item

from config import TH_HAVEN

class LoopCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(minutes=5)
    async def loop(self):
        guild = self.bot.get_guild(TH_HAVEN)

        rewards = []
        reward_choices = ["wood_crate", "iron_crate"]

        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:
                if member.bot:
                    continue

                item_id = random.choices(reward_choices, weights=[90, 10])[0]
                rewards.append((member, item_id))

        try:
            with database.atomic():
                for member, item_id in rewards:
                    item.give(member, item_id, 1)
                    logger.debug(f"成功給予 {member.id} {item_id} x1")

        except Exception as e:
            logger.exception(f"語音獎勵發放失敗：{e}")

    @loop.before_loop
    async def loop_wait(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(LoopCog(bot))