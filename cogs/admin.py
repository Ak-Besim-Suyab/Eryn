import discord
from discord.ext import commands

from ui.views.daily_reward import DailyRewardView

VERIFY_CHANNEL = 1472379536187326464

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def daily_reward(self, ctx: commands.Context):
        # send daily reward message to announcement channel
        lines = [
            "咪！旅人可以在每天 12 點過後，點擊下方的按鈕簽到喵！",
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
        await ctx.send('咪... 要睡覺嚕ZZzz...')
        print("機器人已關閉。")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))