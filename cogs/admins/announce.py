import discord 
from discord.ext import commands
from discord import app_commands

from ui.views import AttendanceView

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    notice_group = app_commands.Group(
        name="notice", 
        description="發布管理者公告"
    )

    @notice_group.command(
        name="attendance", 
        description="發布每日簽到公告"
    )
    @app_commands.default_permissions(administrator=True)
    async def attendance(self, interaction: discord.Interaction):

        descriptions = [
            "歡迎回來，記得每天 12 點過後來這裡簽到喵！咪祝你有美好的一天！",
            "",
            "> 點擊「狀態」可以查看個人狀態",
            "> 點擊「排名」可以查看等級與經驗值排名"
        ]
        
        embed = discord.Embed()
        embed.title = "每日簽到"
        embed.description = "\n".join(descriptions)
        embed.color = discord.Color.gold()

        view = AttendanceView()
        await interaction.response.send_message(embed=embed, view=view)

    
    @notice_group.command(
        name="season", 
        description="發布限時活動公告"
    )
    @app_commands.default_permissions(administrator=True)
    async def notice_season(self, interaction: discord.Interaction) -> None:
        return None

async def setup(bot):
    await bot.add_cog(AnnounceCog(bot))