import discord
from discord.ext import commands
from discord import app_commands

from views import passport

class PassportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="護照", description="查看旅人在本社群的各項數據與紀錄")
    @app_commands.describe(member="要查詢的旅人（僅管理員可用）")
    async def info_command(self, interaction: discord.Interaction, member: discord.Member = None):

        if member is not None and member.id != interaction.user.id and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("只有管理員才能查看別人的護照喔！", ephemeral=True)
            return

        await passport.show(interaction, member)

async def setup(bot: commands.Bot):
    await bot.add_cog(PassportCog(bot))