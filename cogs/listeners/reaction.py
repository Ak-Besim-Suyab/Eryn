import discord
from discord.ext import commands

from cores.logger import logger

from session.level_session import LevelSession

class ReactionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = LevelSession(bot)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):

        # 忽略機器人反應
        if reaction.member and reaction.member.bot:
            return
        
        self.session.give_reaction_experience(reaction.member)
        
        logger.info(f'{reaction.member} 在訊息 {reaction.message_id} 添加反應：{reaction.emoji}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction: discord.RawReactionActionEvent):
        # 這裡有個需要注意的事項：
        # 在 remove 事件中, Discord 不會提供 reaction.member (因為該成員可能已經退群)
        # 所以你只能拿到 user_id。如果需要 User/Member 物件，必須手動獲取

        logger.info(f'{reaction.member} 收回在訊息 {reaction.message_id} 的反應：{reaction.emoji}')


async def setup(bot):
    await bot.add_cog(ReactionListener(bot))