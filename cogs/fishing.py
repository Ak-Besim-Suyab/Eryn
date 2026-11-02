import discord
from discord.ext import commands
from discord import app_commands

import random

from data import LOOT_TABLES
from lib import item

class FishingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="釣魚", description="於所在地點釣魚")
    async def fishing(self, interaction: discord.Interaction):

        results = self.roll("the_river", times = 3)

        description = ["獲得："]
        for item_id, quantity in results.items():
            description.append(item.summary_line(item_id, quantity))

        await interaction.response.send_message("\n".join(description))

    def roll(self, pool_name: str, times: int = 1):
        pool = LOOT_TABLES.get(pool_name)
        results = {}
        for _ in range(times):
            result = random.choices(pool.entries, weights=[loot.weight for loot in pool.entries], k=1)[0]
            results[result.id] = results.get(result.id, 0) + random.randint(result.min, result.max)

        return results

async def setup(bot: commands.Bot):
    await bot.add_cog(FishingCog(bot))