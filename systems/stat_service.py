import discord
import json
from pathlib import Path

from models.player import Player
from models.message import message_manager 

class StatService:
    async def view(self, interaction: discord.Interaction):
        player = Player.get_or_create_player(interaction.user.id)
        stat = player.stats.get()
        houses = self.get_houses(interaction)

        # 房屋敘述
        house_value = []

        if houses:
            for house_id in houses:
                house_value.append(f"- <#{house_id}>")
        else:
            house_value.append("- *尚未擁有任何小屋*")

        payload = {
            "level": player.level,
            "experience": player.experience,
            "currency": player.currency,
            "total_daily_claims": stat.total_daily_claims,
            "house_value": "\n".join(house_value)
        }

        # 印出訊息
        embed = message_manager.create("stat", payload=payload, interaction=interaction)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    def get_houses(self, interaction: discord.Interaction):
        file = Path(f"data/members/{interaction.user.id}.json")
        if file.exists():
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                houses = data.get("house", [])
                return houses