import discord
from models.player import Player

class LeaderboardMenu:
    @staticmethod
    async def show(interaction: discord.Interaction):

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