import discord
import random
import asyncio
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

        # ignore another discord bot.
        if member.bot:
            return

        messages = [
            "歡迎你來到 Th Haven！",
            "剛加入的成員都會收到我 —— 社群管家的歡迎訊息",
            "如果有任何問題或想知道的事情，都可以問我！"
        ]

        try:
            for msg in messages:
                # delay = random.uniform(1.5, 3.0)

                async with member.typing():
                    await asyncio.sleep(5.0)

                await member.send(msg)

        except discord.Forbidden:
            print(f"嘗試私訊新成員 {member} 失敗，新成員可能已關閉私訊設定。")

        ########################
        # embeds = embed_builder.create("member_join", 
        #     author = member.display_name,
        #     portrait = member.display_avatar.url,
        #     parameters = {
        #     }
        # )

        line = random.choice(WELCOME_MESSAGES)

        embed = discord.Embed(
            title=f"{member.display_name}，歡迎來到 Th Haven！",
            description=line,
            color=discord.Color(0xA0C8FF)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        embed_eryn = discord.Embed(
            title=f"",
            description="「咪也在這裡歡迎旅人的到來。如果旅人的私訊功能已關閉，也可以在這裡詢問咪任何問題或想知道的事情。如果旅人有玩特定遊戲，比如最終幻想時，社群有特別的規定需要先瞭解。」\n\n> *選擇對話可以進行互動*",
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