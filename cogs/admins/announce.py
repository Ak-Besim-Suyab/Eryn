import discord 
from discord.ext import commands
from discord import app_commands

from game import context

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
        await context.Context("attendance").send(interaction)
    
    @notice_group.command(
        name="season", 
        description="發布限時活動公告"
    )
    @app_commands.default_permissions(administrator=True)
    async def notice_season(self, interaction: discord.Interaction):
        # dialog = DialogueView(dialog_name="commemorate")
        # await dialog.send(interaction)
        pass

async def setup(bot):
    await bot.add_cog(AnnounceCog(bot))