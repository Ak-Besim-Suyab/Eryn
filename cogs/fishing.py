import discord
from discord.ext import commands
from discord import app_commands

from data import LOOT_TABLES, LINES
from lib.item import summary_line
from lib import view
from lib.util.dice import roll, judge, Outcome
from lib.stat import get_stats

# 職骰結果對應的戰利品獲得次數
fallback = {
    Outcome.CRITICAL_FAILURE: 0,
    Outcome.FAILURE: 0,
    Outcome.SUCCESS: 1,
    Outcome.CRITICAL_SUCCESS: 2
}

class FishingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="釣魚", description="於所在地點釣魚")
    async def fishing(self, interaction: discord.Interaction):

        dice = roll(1, 20)

        loot_table = LOOT_TABLES.get("the_river")
        results = loot_table.roll(3)

        contents = {"display_name": interaction.user.display_name}

        fishes = []
        for (_, item_id), quantity in results.items():
            fishes.append(summary_line(item_id, quantity))

        line = LINES.get("fishing_success")

        contents.update({"dice": dice})
        contents.update({"line": line.random()})
        contents.update({"fishes": "、".join(fishes)})

        await interaction.response.send_message(view=view.create(f"fishing_success", **contents))

async def setup(bot: commands.Bot):
    await bot.add_cog(FishingCog(bot))