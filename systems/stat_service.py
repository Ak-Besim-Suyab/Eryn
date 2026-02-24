import discord

from database.player import Player

from ui.views.stat import StatView

class StatService:
    def __init__(self):
        pass

    async def view(self, interaction: discord.Interaction):
        player = Player.get_or_create_player(interaction.user.id, interaction.user.display_name)
        stat = player.stats.get()

        description = [
            f"活躍度等級: {player.level}",
            f"活躍度經驗值: {player.experience}",
            f"",
            f"累計簽到天數: {stat.total_daily_claims} 天"
        ]

        embed = discord.Embed(
            title = interaction.user.display_name,
            description = "\n".join(description),
            color = discord.Color.dark_gold()
        )
        embed.set_author(url=interaction.user.avatar.url)

        view = StatView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)