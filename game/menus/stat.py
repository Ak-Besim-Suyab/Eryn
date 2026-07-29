import discord
from models import Player
from models import Statistic

class StatMenu:
    @staticmethod
    async def show(interaction: discord.Interaction):

        user_id = interaction.user.id

        player = Player.get_or_create_player(user_id)
        stat = Statistic.get_or_create_stat(user_id)

        descriptions = [
            f"等級: {player.level}",
            f"經驗值: {player.experience}",
            f"",
            f"累計簽到的天數: {stat.total_daily_claims} 天",
            f"累計發送的訊息數: {stat.total_message_send} 次",
            f"累計語音時間: {stat.total_voice_time} 分鐘",
        ]

        embed = discord.Embed()
        embed.description = "\n".join(descriptions)
        embed.color = discord.Color.gold()

        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)