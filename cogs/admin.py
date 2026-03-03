import discord
from discord.ext import commands
from pathlib import Path

from cores.logger import logger

from ui.views.daily_reward import DailyRewardView

VERIFY_CHANNEL = 1472379536187326464

MEMBER_PATH = "data/members"

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context):
        embed = discord.Embed(
            title="測試指令",
            description="測試",
            color=discord.Color.gold()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def daily_reward(self, ctx: commands.Context):
        # send daily reward message to announcement channel
        lines = [
            "咪！旅人可以在每天 12 點過後，點擊下方的按鈕簽到！",
            "",
            "> 如果想確認簽到狀態，可以點擊「狀態」按鈕查看",
        ]
        embed = discord.Embed(
            title="每日簽到",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        view = DailyRewardView(self.bot)
        announcement_channel = self.bot.get_channel(VERIFY_CHANNEL)  # 替換為公告頻道的ID
        await announcement_channel.send(embed=embed, view=view)

# info group -----------------------------------------

    @commands.group()
    @commands.is_owner()
    async def info(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("請指定子指令，使用 `!info list` 列出所有成員的資料檔案狀態")

    @info.command(name="user")
    @commands.is_owner()
    async def user(self, ctx: commands.Context, member: discord.Member):
        file = Path(f"{MEMBER_PATH}/{member.id}.json")
        if file.exists():
            await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Exists")
        else:
            await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Missing")

    @info.command(name="list")
    @commands.is_owner()
    async def list(self, ctx: commands.Context):
        guild = ctx.guild
        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if file.exists():
                await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Exists")
            else:
                await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Missing")
    
    @info.command(name="file_exist")
    @commands.is_owner()
    async def exist(self, ctx: commands.Context):
        guild = ctx.guild
        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if file.exists():
                await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Exists")

    @info.command(name="file_missing")
    @commands.is_owner()
    async def missing(self, ctx: commands.Context):
        total = 0
        guild = ctx.guild

        for member in guild.members:
            file = Path(f"{MEMBER_PATH}/{member.id}.json")
            if not file.exists():
                await ctx.send(f"MEMBER - {member.display_name} | ID - {member.id} | FILE - Missing")
#----------------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功重新載入 cogs.{cog}')
        except commands.ExtensionNotFound:
            await ctx.send(f'❌ 找不到 cogs.{cog} 喵')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法重新載入 cogs.{cog}：{e}')


    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功載入 cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'❌ cogs.{cog} 已經載入喵')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法載入 cogs.{cog}：{e}')


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.unload_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功卸載 cogs.{cog}')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'❌ cogs.{cog} 未載入，無法卸載喵')
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
                level_session.settle_voice_experience(member)
        await ctx.send('咪... 要睡覺嚕ZZzz...')
        logger.info("機器人已關閉。")

        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))