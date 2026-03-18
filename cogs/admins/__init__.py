import discord
from discord.ext import commands
from pathlib import Path

from cores.logger import logger

from ui.daily import DailyEmbed, DailyView
from ui.season_event import SeasonEventView

VERIFY_CHANNEL = 1472379536187326464

MEMBER_PATH = "data/members"

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.color = discord.Color.gold()
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="test", value="test")

        await ctx.send(embed=embed)

# daily message --------------------------------------------------------------
    @commands.command()
    @commands.is_owner()
    async def daily(self, ctx: commands.Context):

        embed = DailyEmbed()
        view = DailyView()

        announcement_channel = self.bot.get_channel(VERIFY_CHANNEL)  # 替換為公告頻道的ID
        await announcement_channel.send(embed=embed, view=view)
# ----------------------------------------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def season_event(self, ctx: commands.Context):
        description = "\n".join([
            "*「你們怎麼都打那麼久，我兩場就過了欸」-2026/3/5 14:30*",
            "",
            "　　　　　 🕯️紀念偉大的勇士 <@600603497330901004>🕯️",
            "",
            "> 點擊「緬懷」可以為勇士的英勇犧牲默哀，有機率功德爆發",
        ])

        embed = discord.Embed(description=description, color=discord.Color.dark_purple())
        embed.set_image(url="https://i.imgur.com/EXAMPLE.png")  # 替換為實際圖片URL

        view = SeasonEventView()

        announcement_channel = self.bot.get_channel(VERIFY_CHANNEL)
        await announcement_channel.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))