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
    async def announcement(self, interaction: discord.Interaction):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("你沒有權限使用這個指令（需要管理員權限）", ephemeral=True)

        embed = discord.Embed(
            title="Eryn 系統公告",
            description="這是一則示範用的公告訊息。",
            color=discord.Color.blue()
        )

        embed.set_footer(text="由 Eryn Bot 發送")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Announcement(bot))