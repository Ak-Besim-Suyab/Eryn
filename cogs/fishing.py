import discord
from discord.ext import commands
from discord import app_commands

from data import LOOT_TABLES, LINES
from lib.item import summary_line
from lib.view import create_view

class FishingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="釣魚", description="於所在地點釣魚")
    async def fishing(self, interaction: discord.Interaction):

        loot_table = LOOT_TABLES.get("the_river")
        results = loot_table.roll(3)

        contents = {"display_name": interaction.user.display_name}

        fishes = []
        for (_, item_id), quantity in results.items():
            fishes.append(summary_line(item_id, quantity))

        line = LINES.get("fishing_success")

        contents.update({"line": line.random()})
        contents.update({"fishes": "、".join(fishes)})

        await interaction.response.send_message(view=create_view(f"fishing_success", **contents))

async def setup(bot: commands.Bot):
    await bot.add_cog(FishingCog(bot))