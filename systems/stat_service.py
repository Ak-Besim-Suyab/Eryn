import discord
import json
from pathlib import Path

from database.player import Player

class StatService:

    async def view(self, interaction: discord.Interaction):
        player = Player.get_or_create_player(interaction.user.id, interaction.user.display_name)
        stat = player.stats.get()
        houses = self.get_houses(interaction)

        lines = [
            f"等級: {player.level}",
            f"經驗值: {player.experience}",
            f"",
            f"累計簽到天數: {stat.total_daily_claims} 天",
            f""
        ]

        house_lines = [
            f"已擁有的小屋："
        ]
        if houses:
            for house_id in houses:
                house_lines.append(f"- <#{house_id}>")
        else:
            house_lines.append("- *尚未擁有任何小屋*")

        title = None
        description = "\n".join(lines + house_lines)
        color = discord.Color.dark_gold()

        embed = discord.Embed(title = title, description = description, color = color)
        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)

        await interaction.response.send_message(embed = embed, ephemeral = True)

    def get_houses(self, interaction: discord.Interaction):
        file = Path(f"data/members/{interaction.user.id}.json")
        if file.exists():
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                houses = data.get("house", [])
                return houses