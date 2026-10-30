import random
import discord
from discord.ext import commands

from lib.utils import dice

from config import MAX_SIDES

class MessageDiceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return

        if (d := dice.parse(message.content)) is None:
            return

        count, sides = d

        # 檢查面數是否超過最大限制
        if sides > MAX_SIDES:
            return
        
        rolls = [random.randint(1, sides) for _ in range(count)]

        if count == 1:
            reply = f"🎲 {rolls[0]}"
        else:
            reply = f"🎲 {sum(rolls)} ({' + '.join(map(str, rolls))})"

        await message.reply(reply, mention_author=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(MessageDiceListener(bot))