import random
import discord
from discord.ext import commands

from lib.emoji_dice import count_emoji

random_stick = [
    "<:dai_kichi:1561975565500817428>",
    "<:kichi:1561975597335314542>",
    "<:sho_kichi:1561975608949481542>",
    "<:sho_kyo:1561975734153781318>",
    "<:kyo:1561975744417239050>",
    "<:dai_kyo:1561975786398023780>",
]

class EmojiDiceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if message.author.bot:
            return

        num = count_emoji(message.content, '1561963940689354852')
        if num == 0:
            return

        reply = ""

        for i in range(num):
            reply += random.choice(random_stick)

        await message.reply(reply, mention_author=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiDiceListener(bot))