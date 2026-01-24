import discord

from cogs.engines.fishing_engine import FishingEngine
from utils.logger import logger
from context import Context


class FishingAgainButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="再釣一次", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        engine = FishingEngine()
        payload = engine.cast(interaction)

        if not payload:
            await interaction.response.send_message("你什麼都沒釣到...", ephemeral=True)
            return

        item_manager = Context.get_manager("item")
        lines = []
        
        for item in payload:
            item_obj = item_manager.get_item(item["item_id"])
            item_name = item_obj.name if item_obj else item["item_id"]
            lines.append(f"**{item_name}**× {item['quantity']}")

        embed = discord.Embed(
            title="你釣到...",
            description="\n".join(lines),
            color=discord.Color.blue()
        )

        new_view = type(self.view)()
        await interaction.response.send_message(embed=embed, view=new_view)