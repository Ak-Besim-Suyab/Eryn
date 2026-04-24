import discord
from discord.ext import commands

from game.systems import LevelSystem

class ReactionListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: discord.RawReactionActionEvent):
        
        # 忽略機器人反應
        if reaction.member and reaction.member.bot:
            return
        
        LevelSystem.give_reaction_experience(reaction.member)

async def setup(bot):
    await bot.add_cog(ReactionListener(bot))