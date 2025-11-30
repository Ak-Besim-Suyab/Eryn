import discord
import random
from discord.ext import commands

MESSAGES = [
    "很高興你降落到此，希望你會喜歡這裡 🎉",
    "很高興你的到來，希望你會喜歡這裡 🎉",
]

class TestEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test_embed")
    async def test_embed(self, ctx: commands.Context):

        line = random.choice(MESSAGES)

        embed = discord.Embed(
            title=f"{ctx.author.display_name}，歡迎來到 Th Haven！",
            description=line,
            color=discord.Color(0xA0C8FF)
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        # embed.set_author(
        #     name=ctx.author.display_name,
        #     icon_url=ctx.author.display_avatar.url
        # )
        embed.timestamp = discord.utils.utcnow()

        embed_eryn = discord.Embed(
            title=f"",
            description="「初次見面，咪是社群的獨門管家，大部分事務未來都將會由咪託管，請多多關照。」\n\n*社群有許多實用且有趣的小功能讓旅人探索，如果旅人想知道某些功能的詳細內容，都可以隨時輸入指令，或者按下方的按鈕聽取說明。*",
            color=discord.Color(0xA0C8FF)
        )
        embed_eryn.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed_eryn.set_author(
            name=self.bot.user.display_name,
            icon_url=self.bot.user.display_avatar.url
        )
        embed_eryn.timestamp = discord.utils.utcnow()

        await ctx.send(embeds=[embed, embed_eryn])

async def setup(bot):
    await bot.add_cog(TestEmbed(bot))