"""
這個類別用來創建 /公告 指令
/公告頻道 加入 ID
/公告頻道 刪除
"""
import discord 
from discord.ext import commands
from discord import app_commands

from models.guild import Guild

class SettingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    setting_group = app_commands.Group(
        name="設定", 
        description="伺服器對於機器人的相關設定"
    )

    announcement_channel_group = app_commands.Group(
        name="公告頻道", 
        description="設定艾琳用來發送廣播訊息的頻道 （需要管理者權限）", 
        parent=setting_group
    )
    
    @announcement_channel_group.command(
        name="新增", 
        description="新增公告頻道，這個頻道會用來推播艾琳的遊戲所要發送的公共訊息"
    )
    @app_commands.describe(channel="要設定的頻道")
    @app_commands.default_permissions(administrator=True)
    async def set_announcement_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        Guild.set_announcement_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(f"已設定公告頻道為 {channel.mention}", ephemeral=True)

    @announcement_channel_group.command(
        name="刪除", 
        description="刪除公告頻道"
    )
    async def delete_announcement_channel(self, interaction: discord.Interaction):
        channel = Guild.get_announcement_channel(interaction.guild.id)
        if not channel:
            await interaction.response.send_message("目前沒有已設定的公告頻道可以移除。", ephemeral=True)
            return
        Guild.set_announcement_channel(interaction.guild.id, None)
        await interaction.response.send_message(f"已移除公告頻道。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SettingCog(bot))