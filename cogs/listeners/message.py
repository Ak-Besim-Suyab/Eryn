import asyncio
import discord
from discord.ext import commands

from ui.views.role_setting_view import RoleSettingView

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        keywords = [
            "艾琳"
        ]

        content = message.content.strip().lower()

        for keyword in keywords:
            if keyword in content:
                await message.channel.send(f"喵！{message.author.display_name} 叫咪嗎？")
            else:
                # 未搜尋到關鍵字，不往下執行
                return

        def check(m):
                return m.author == message.author and m.channel == message.channel

        try:
            reply = await self.bot.wait_for('message', check=check, timeout=30.0)
            reply_content = reply.content.strip().lower()

            if "身分組" in reply_content and ("設定" in reply_content or "打開" in reply_content or "開啟" in reply_content):

                async with message.channel.typing():
                    await asyncio.sleep(3.0)

                await message.channel.send(f"咪！找找... 找找...")

                async with message.channel.typing():
                    await asyncio.sleep(3.0)

                await message.channel.send(f"咪找到好多設定按鈕... 嗷嚕嚕通通都給你喵！", view=RoleSettingView())

        except asyncio.TimeoutError:
            print("等待回覆超時，未收到使用者的回覆。")

async def setup(bot):
    await bot.add_cog(Message(bot))