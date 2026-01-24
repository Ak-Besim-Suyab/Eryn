import discord
from discord import app_commands
from discord.ext import commands

from engines.fishing_engine import FishingEngine
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM, Context


class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="釣魚", description="在你所處的地點釣魚")
    async def fishing(self, interaction: discord.Interaction):
        
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

        view = Context.get_manager("view").create("fishing_view")
 
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Fishing(bot))

