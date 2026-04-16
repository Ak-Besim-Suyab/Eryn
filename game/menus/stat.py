import discord
from models.player import Player

class StatMenu:
    @staticmethod
    async def show(interaction: discord.Interaction):

        player = Player.get_or_create_player(interaction.user.id)
        stat = player.stats.get()

        descriptions = [
            f"等級: {player.level}",
            f"經驗值: {player.experience}",
            f"",
            f"累計簽到天數: {stat.total_daily_claims} 天"
        ]

        embed = discord.Embed()
        embed.description = "\n".join(descriptions)
        embed.color = discord.Color.gold()

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)