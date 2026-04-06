import discord

from models.data.item import item_manager

class GardenEmbed(discord.Embed):
    def __init__(self, interaction: discord.Interaction, result: dict):
        super().__init__()

        self.description = "採集成功！"
        self.color = discord.Color.gold()

        lines = []
        for item_id, quantity in result.items():
            item = item_manager.get(item_id)
            lines.append(f"{item.image}{item.name} x{quantity}")

        self.add_field(name="獲得物品：", value="\n".join(lines), inline=False)

        self.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)