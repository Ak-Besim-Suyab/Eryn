from discord.ext import commands
from discord import ui

import data
from lib import builder

"""此元件用於管理與發送公告和測試訊息
"""
class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def announce(self, ctx: commands.Context, message_name: str):
        container_data = data.container.get(message_name)
        if container_data is None:
            await ctx.send(f"❌ 找不到名為 {message_name} 的訊息")
            return

        # 這個片段用於測試參數傳入, 非指定測試文本則留空
        param = {}
        if message_name == "template_param":
            param = {
                "name": "Elin",
                "level": 1,
                "experience": 100
            }
        
        view = ui.LayoutView(timeout = None).add_item(builder.build_container(container_data, **param))
        await ctx.send(view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))