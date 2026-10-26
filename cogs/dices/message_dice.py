import random
import discord
from discord.ext import commands

from config import DICE_PATTERN
from config import MAX_SIDES

class MessageDiceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return

        match = DICE_PATTERN.match(message.content)
        if not match:
            return

        # 取得匹配數量與面數
        count = int(match.group(1) or 1)
        sides = int(match.group(2))

        # 檢查擲骰數量與面數, 數量不能小於 1 (0D10 為無效擲骰), 面數必須小於最大面數 (控制項), 面數不能小於 2 (1D1 為無效擲骰)
        if count < 1 or sides > MAX_SIDES or sides < 2:
            return
        
        rolls = [random.randint(1, sides) for _ in range(count)]

        if count == 1:
            reply = f"🎲 {rolls[0]}"
        else:
            reply = f"🎲 {sum(rolls)} ({' + '.join(map(str, rolls))})"

        await message.reply(reply, mention_author=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(MessageDiceListener(bot))