from discord.ext import commands, tasks

from cores import logger
from lib.system import reward

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
        if guild is None:
            return

        member_ids = [
            member.id
            for voice_channel in guild.voice_channels
            for member in voice_channel.members
            if not member.bot
        ]

        try:
            reward.give_region_rewards(member_ids)
        except Exception as e:
            logger.exception(f"語音獎勵發放失敗：{e}")

    @loop.before_loop
    async def loop_wait(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(LoopCog(bot))