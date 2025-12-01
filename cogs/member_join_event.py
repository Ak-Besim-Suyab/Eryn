import discord
import random
from discord.ext import commands

from ui.selects.cat_select import CatSelectView

WELCOME_MESSAGES = [
    "很高興你降落到此，希望你會喜歡這裡 🎉",
    "很高興你的到來，希望你會喜歡這裡 🎉",
]

class MemberJoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        line = random.choice(WELCOME_MESSAGES)

        embed = discord.Embed(
            title=f"{member.display_name}，歡迎來到 Th Haven！",
            description=line,
            color=discord.Color(0xA0C8FF)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        # embed.set_author(
        #     name=member.display_name,
        #     icon_url=member.display_avatar.url
        # )
        embed.timestamp = discord.utils.utcnow()

        embed_eryn = discord.Embed(
            title=f"",
            description="「咪也歡迎您的到來。有任何問題或想知道的事情都可以詢問咪。如果旅人有玩特定遊戲，比如最終幻想時，社群有特別的規定需要先瞭解。」\n\n> *選擇下方選單裡的選項可以進行互動*",
            color=discord.Color(0xA0C8FF)
        )
        embed_eryn.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed_eryn.set_author(
            name=self.bot.user.display_name,
            icon_url=self.bot.user.display_avatar.url
        )
        embed_eryn.timestamp = discord.utils.utcnow()

        view = CatSelectView()

        channel = member.guild.system_channel
        if channel:
            await channel.send(embeds=[embed, embed_eryn], view=view)

async def setup(bot):
    await bot.add_cog(MemberJoinEvent(bot))