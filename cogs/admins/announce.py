import discord 
from discord.ext import commands
from discord import app_commands

from systems import sessions

class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    announce_group = app_commands.Group(
        name="announce", 
        description="發布管理者公告"
    )

    @announce_group.command(name="attendance", description="發布每日簽到公告")
    @app_commands.default_permissions(administrator=True)
    async def attendance(self, interaction: discord.Interaction):
        session = sessions.DialogueSession("attendance")
        await session.send(interaction)
    
    @announce_group.command(name="season", description="發布限時活動公告")  
    @app_commands.default_permissions(administrator=True)
    async def notice_season(self, interaction: discord.Interaction):
        # dialog = DialogueView(dialog_name="commemorate")
        # await dialog.send(interaction)
        pass

    @commands.command()
    @commands.is_owner()
    async def character_setting(self, ctx: commands.Context):
        session = sessions.DialogueSession("character_setting")
        await session.send(ctx)

async def setup(bot: commands.Bot):
    await bot.add_cog(AnnounceCog(bot))