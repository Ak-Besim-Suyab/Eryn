"""
此元件實作熱載其他 Cog 元件，以及安全關閉機器人的指令。
"""
from discord.ext import commands
from cores.logger import logger

class BootCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        from game.systems import LevelSystem
        for member in guild.members:
            if member.voice and member.voice.channel:
                if member.bot:
                    continue
                LevelSystem.give_voice_experience(member)

        logger.info("機器人已關閉。")

        await self.bot.close()


async def setup(bot):
    await bot.add_cog(BootCog(bot))