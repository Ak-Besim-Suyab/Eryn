import discord
from discord.ext import commands

BOT_CHANNEL_ID = 1450110904912969800

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_leveling(self, user, skill_name: str, skill_level: int):
        """
        等級提升監聽
        升級時，於指定頻道發送消息

        需要傳入的參數：
        user: 使用者物件，可能型別： interaction.user 或 message.author
        skill_name: 提升的技能名稱
        skill_level: 提升後的技能等級

        目前應用的類別：
        - session.fishing_session.FishingSession
        - session.level_session.LevelSession
        """ 
        # 取得頻道對象
        channel = self.bot.get_channel(BOT_CHANNEL_ID)
        if not channel:
            print(f"無法找到頻道 ID: {BOT_CHANNEL_ID}")
            return

        # 發送消息
        embed = discord.Embed(
            title="等級提升！",
            description=f"{skill_name}等級提升至 {skill_level}！",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))