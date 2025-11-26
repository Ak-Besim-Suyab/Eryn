import discord
from discord import app_commands
from discord.ext import commands

from context import Context

class Announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Command loaded: announcement')

    @app_commands.guilds(Context.GUILD_TH_HAVEN, Context.GUILD_AK_BESIM)
    @app_commands.command(name="announcement", description="發送公告（僅由管理員使用）")
    @app_commands.describe(channel="要發送公告的頻道")
    async def announcement(self, interaction: discord.Interaction, channel: discord.TextChannel):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("你沒有權限使用這個指令（需要管理員權限）", ephemeral=True)

        lines = [
            "歡迎旅人來到避風港（Th Haven）遊玩與定居，這裡是綜合向社群！",
            "旅人可以在這裡和大家玩遊戲、討論動漫電影，以及分享自己的生活！",
            "",
            "這裡是愛爾琳（Eryn）—— 社群的管理員",
            "旅人對社群有任何問題或想知道的事情，都歡迎點選下方按鈕或輸入指令查看哦！",
        ]

        embed = discord.Embed(
            title="旅居手冊",
            description="\n".join(lines),
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1193049715638538283/1443018531741634703/image.png")

        await channel.send(embed=embed)

        await interaction.response.send_message(f"公告已成功發送至 {channel.mention}。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announcement(bot))