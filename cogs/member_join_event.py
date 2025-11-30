import discord
import random
from discord.ext import commands

WELCOME_MESSAGES = [
    "很高興你降落到此，希望你會喜歡這裡！\n\n群有許多實用與有趣的小功能讓旅人探索，想知道這些功能的詳細內容，都可以按下方的按鈕聽取說明哦！",
    "很高興你的到來，希望你會喜歡這裡！\n\n群有許多實用與有趣的小功能讓旅人探索，想知道這些功能的詳細內容，都可以按下方的按鈕聽取說明哦！",
]

class MemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        line = random.choice(WELCOME_MESSAGES)

        embed = discord.Embed(
            title=f"🎉 {member.display_name}，歡迎來到 Th Haven！",
            description=line,
            color=discord.Color(0xA0C8FF)
        )

        # embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(
            name=member.display_name,
            icon_url=member.display_avatar.url
        )

        embed.timestamp = discord.utils.utcnow()

        channel = member.guild.system_channel
        if channel:
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberJoinEvent(bot))