import discord
import json
from pathlib import Path

from models.player import Player

class StatService:

    async def view(self, interaction: discord.Interaction):
        player = Player.get_or_create_player(interaction.user.id)
        stat = player.stats.get()
        houses = self.get_houses(interaction)

        lines = [
            f"等級：{player.level}",
            f"經驗值：{player.experience}",
            f"金幣：{player.currency}",
            f"",
            f"累計簽到天數：{stat.total_daily_claims} 天",
            f""
        ]

        # 房屋敘述
        house_description = []

        if houses:
            for house_id in houses:
                house_description.append(f"- <#{house_id}>")
        else:
            house_description.append("- *尚未擁有任何小屋*")

        # 印出訊息
        embed = discord.Embed()
        embed.description = "\n".join(lines)
        embed.color = discord.Color.dark_gold()

        embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.avatar.url)

        embed.add_field(name = "已擁有的小屋：", value = "\n".join(house_description), inline = False)

        await interaction.response.send_message(embed = embed, ephemeral = True)

    def get_houses(self, interaction: discord.Interaction):
        file = Path(f"data/members/{interaction.user.id}.json")
        if file.exists():
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                houses = data.get("house", [])
                return houses