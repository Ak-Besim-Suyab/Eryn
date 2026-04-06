import discord
from discord.ext import commands
from discord import app_commands
from models.player import Player

from configuration import GUILD_AK_BESIM, GUILD_TH_HAVEN

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="排名", description="查看成員排名")
    async def execute(self, interaction: discord.Interaction):
        await self.show_leaderboard(interaction)

    async def show_leaderboard(self, interaction: discord.Interaction):
        tops = Player.select().order_by(
            Player.level.desc(), 
            Player.experience.desc()
        ).limit(10)

        embed = discord.Embed()
        embed.title = "活躍度排名"
        embed.description = "依照等級與經驗值排序，顯示前 10 名社群成員"
        embed.color = discord.Color.gold()

        top_lines = []
        for index, player in enumerate(tops, start=1):
            member = interaction.guild.get_member(player.id)
            if member:
                top_lines.append(f"**{index}. {member.display_name}** 等級 {player.level} / {player.experience} Exp")

        embed.add_field(name="", value="\n".join(top_lines), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))