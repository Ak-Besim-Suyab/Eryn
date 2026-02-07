import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功重新載入 cogs.{cog}')
        except commands.ExtensionNotFound:
            await ctx.send(f'❌ 找不到 cogs.{cog} 喵')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法重新載入 cogs.{cog}：{e}')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        try:
            await self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'✅ 咪！成功載入 cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'❌ cogs.{cog} 已經載入喵')
        except Exception as e:
            await ctx.send(f'❌ 咪... 無法載入 cogs.{cog}：{e}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
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