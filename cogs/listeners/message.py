from datetime import datetime

import discord
from discord.ext import commands

import config
from cores import logger
from lib import level_system, player
from lib.system import reward

MESSAGE_EXPERIENCE = 5

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns: dict[int, float] = {}

    def _is_on_cooldown(self, user_id: int) -> bool:
        """
        檢查玩家是否仍在訊息獎勵冷卻時間內，若未在冷卻內則更新時間戳
        """
        now = datetime.now().timestamp()
        last = self.cooldowns.get(user_id)
        if last is not None and now - last < config.MESSAGE_COOLDOWN:
            return True

        self.cooldowns[user_id] = now
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # 忽略機器人訊息與私人訊息，這個判斷會確保 message.author 指向 discord.Member
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id

        player_stat = player.get_statistic(user_id)
        player_stat.total_message += 1
        player_stat.save()

        if self._is_on_cooldown(user_id):
            return

        # 給予訊息經驗值
        bonus = level_system.get_sanctuary_bonus("food", 0.02)
        total_experience = round(MESSAGE_EXPERIENCE * bonus, 2)
        player.add_experience(user_id, total_experience)

        # 給予地區探索獎勵
        reward.give_region_reward(user_id)

        logger.debug(f"給予 {message.author.display_name} 訊息經驗值: {total_experience} exp (倍率: {bonus:.2f}x)")

async def setup(bot):
    await bot.add_cog(MessageListener(bot))