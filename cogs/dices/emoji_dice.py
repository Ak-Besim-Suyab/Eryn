import random
import discord
from discord.ext import commands

from lib.utils import emoji

from config import OMIKUJI_POOL

class EmojiDiceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return

        num = emoji.count(message.content, '1561963940689354852')
        if num == 0:
            return

        reply = ""
        for _ in range(num):
            reply += random.choice(OMIKUJI_POOL)

        await message.reply(reply, mention_author=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiDiceListener(bot))