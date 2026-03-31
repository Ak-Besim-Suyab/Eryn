import discord
from discord.ext import commands

from systems.level_session import LevelSession

from cores.logger import logger

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = LevelSession(bot)

        self.message_cooldown = 30
        self.message_exp = 5
        self.message_cooldowns = {}

        self.reaction_cooldown = 30
        self.reaction_exp = 5
        self.reaction_cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # 忽略機器人訊息與私人訊息，這個判斷會確保 message.author 指向 discord.Member
        if message.author.bot or not message.guild:
            return
        
        self.session.give_message_experience(message.author)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        
        # 忽略機器人反應
        if reaction.member and reaction.member.bot:
            return
        
        self.session.give_reaction_experience(reaction.member)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):

        # 忽略機器人進出語音
        if member.bot:
            return
        
        # 語音狀態檢查
        if after.channel and not before.channel:
            self.session.save_timestamp(member)
            logger.debug(f"[語音] {member.display_name} 加入語音頻道：{after.channel.name}")
            
        elif before.channel and not after.channel:
            self.session.give_voice_experience(member)
            self.session.remove_timestamp(member)
            logger.debug(f"[語音] {member.display_name} 離開語音頻道：{before.channel.name}")


async def setup(bot):
    await bot.add_cog(Leveling(bot))
