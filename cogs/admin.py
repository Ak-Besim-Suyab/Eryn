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

        embed = discord.Embed(color=discord.Color.gold())
        embed.title = "限時活動"
        embed.description = description
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1193049715638538283/1479100041665839227/img_1.png")

        view = SeasonEventView(self.bot)

        await ctx.send(embed=embed, view=view)

# file group -----------------------------------------
    @commands.group()
    @commands.is_owner()
    async def file(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            logger.info("請指定子指令，使用 `!file list` 列出所有成員的資料檔案狀態")


    @file.command(name="list")
    @commands.is_owner()
    async def list(self, ctx: commands.Context):
        guild = ctx.guild
        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if file.exists():
                logger.info(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Exists")
            else:
                logger.info(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Missing")

    @file.command(name="exist")
    @commands.is_owner()
    async def exist(self, ctx: commands.Context):
        guild = ctx.guild
        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if file.exists():
                logger.info(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Exists")

    @file.command(name="missing")
    @commands.is_owner()
    async def missing(self, ctx: commands.Context):
        total = 0
        guild = ctx.guild

        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if not file.exists():
                logger.info(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Missing")

    @commands.command()
    @commands.is_owner()
    async def leaved_member(self, ctx: commands.Context):
        leaved_member_ids = set()
        guild = ctx.guild

        for member in guild.members:
            leaved_member_ids.add(member.id)

        for file in Path(MEMBER_PATH).glob("*.json"):
            user_id = int(file.stem)
            if user_id not in leaved_member_ids:
                logger.info(f"LEAVED MEMBER - ID: {user_id} | FILE: {file.name}")

#----------------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def show_voice_channel(self, ctx: commands.Context):
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel):
                logger.info(f"印出語音頻道: {channel.name}")

#----------------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功重新載入 cogs.{cog}')
        except commands.ExtensionNotFound:
            await ctx.send(f'❌ 找不到 cogs.{cog}')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法重新載入 cogs.{cog}：{e}')


    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功載入 cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'❌ cogs.{cog} 已經載入')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法載入 cogs.{cog}：{e}')


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功卸載 cogs.{cog}')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'❌ cogs.{cog} 未載入，無法卸載')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法卸載 cogs.{cog}：{e}')


    @commands.command()
    @commands.is_owner()
    async def close(self, ctx: commands.Context):

        guild = ctx.guild

        from session.level_session import LevelSession
        level_session = LevelSession(self.bot)
        for member in guild.members:
            if member.voice and member.voice.channel:
                if member.bot:
                    continue
                level_session.give_voice_experience(member)

        logger.info("機器人已關閉。")

        await self.bot.close()


async def setup(bot):
    await bot.add_cog(AdminCog(bot))