import discord
from discord import app_commands
from discord.ext import commands

from context import Context
from ui.views.community_view import CommunityView

class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Command loaded: announcement')

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(name="announcement", description="發送公告（僅由管理員使用）")
    @app_commands.describe(channel="要發送公告的頻道", content="訊息內容")
    async def announcement(self, interaction: discord.Interaction, channel: discord.TextChannel, content: str):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("你沒有權限使用這個指令（需要管理員權限）", ephemeral=True)

        view = CommunityView()

        await channel.send(content, view=view)

        await interaction.response.send_message(f"公告已成功發送至 {channel.mention}。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announcement(bot))