
import discord
from discord.ext import commands
from utils.logger import logger

class Recording(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_store = {}

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('✅ Recording Cog "登記" 已載入')

    @commands.command(name="登記")
    async def record_text(self, ctx, *, content: str):

        user_name = ctx.author.display_name

        self.data_store[user_name] = content
        
        embed = discord.Embed(
            title="✅ 登記成功",
            description=f"**{user_name}**，輸入的文本已儲存喵。",
            color=discord.Color.green()
        )
        embed.add_field(name="儲存的文本：", value=content, inline=False)
        
        await ctx.send(embed=embed, ephemeral=True)

    @commands.command(name="查看登記")
    async def check_text(self, ctx):

        lines = []

        if self.data_store:
            for user_name, content in self.data_store.items():
                lines.append(f"{user_name}: {content}")

            content = "\n".join(lines)

            embed = discord.Embed(
                title="這裡是所有登記內容：",
                description=content,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ 目前沒有任何登記資料！")

    @commands.command(name="清空登記")
    @commands.has_permissions(administrator=True)
    async def clear_record(self, ctx):
        self.data_store.clear()
        
        embed = discord.Embed(
            title="",
            description="所有的登記紀錄已經被移除。",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Recording(bot))