import discord
from discord.ext import commands

from game.systems import LevelSystem

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        # 忽略機器人訊息與私人訊息，這個判斷會確保 message.author 指向 discord.Member
        if message.author.bot or not message.guild:
            return
        
        LevelSystem.give_message_experience(message.author)

async def setup(bot):
    await bot.add_cog(MessageListener(bot))