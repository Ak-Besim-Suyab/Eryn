from datetime import datetime

import discord
from discord.ext import commands

import config
from cores import logger
from lib import level_system, player
from lib.system import reward

REACTION_EXPERIENCE = 5

class ReactionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns: dict[int, float] = {}

    def _is_on_cooldown(self, user_id: int) -> bool:
        """
        檢查玩家是否仍在反應獎勵冷卻時間內，若未在冷卻內則更新時間戳
        """
        now = datetime.now().timestamp()
        last = self.cooldowns.get(user_id)
        if last is not None and now - last < config.REACTION_COOLDOWN:
            return True

        self.cooldowns[user_id] = now
        return False

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):

        # 忽略私訊或機器人反應
        if not reaction.member or reaction.member.bot:
            return

        user_id = reaction.member.id

        if self._is_on_cooldown(user_id):
            return

        # 給予反應經驗值
        bonus = level_system.get_sanctuary_bonus("wood", 0.02)
        total_experience = round(REACTION_EXPERIENCE * bonus, 2)
        player.add_experience(user_id, total_experience)

        # 給予地區探索獎勵
        reward.give_region_reward(user_id)

        logger.debug(f"給予 {reaction.member.display_name} 反應經驗值: {total_experience} exp (倍率: {bonus:.2f}x)")

async def setup(bot):
    await bot.add_cog(ReactionListener(bot))