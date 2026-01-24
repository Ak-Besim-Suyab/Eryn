import discord
from discord import app_commands
from discord.ext import commands

from engines.fishing_engine import FishingEngine
from context import GUILD_TH_HAVEN, GUILD_AK_BESIM, Context

from utils.event_manager import EventManager


class Fishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = FishingEngine()
        self.event = EventManager()

        # self.event.subscribe("fish.harvested", on_fishing_success)
        # self.event.subscribe("fish.wasted", on_fishing_failed)

    @app_commands.guilds(GUILD_TH_HAVEN, GUILD_AK_BESIM)
    @app_commands.command(name="釣魚", description="在你所處的地點釣魚")
    async def fishing(self, interaction: discord.Interaction):

        event = EventManager()
        event.subscribe("fishing_failed", on_fishing_failed)

        payload = self.engine.cast(interaction)

        view = Context.get_manager("view").create("fishing_view")

        if not payload:
            event.post("fishing_failed", interaction=interaction, view=view)
            return

        item_manager = Context.get_manager("item")
        lines = []

        for item in payload:
            # 判斷是物品還是寶箱
            if "item_id" in item:
                # 普通物品
                item_obj = item_manager.get_item(item["item_id"])
                item_name = item_obj.name if item_obj else item["item_id"]
                lines.append(f"**{item_name}** × {item['quantity']}")

        embed = discord.Embed(
            title = interaction.user.display_name, 
            description = "你在附近的水域垂釣，好像有魚上鉤...", 
            color = discord.Color.blue()
        )
        embed.add_field(name="你獲得：", value="\n".join(lines), inline=False)

        for item in payload:
            if item.get("event_type") == "treasure":
                currency = item.get("currency", 0)
                embed.add_field(
                    name="你在水域附近發現寶藏！",
                    value=f"獲得額外 {currency} 金幣",
                    inline=False
                )
 
        await interaction.response.send_message(embed=embed, view=view)

async def on_fishing_failed(interaction: discord.Interaction, view):
    embed = discord.Embed(
        title=interaction.user.display_name,
        description="你在附近的水域垂釣，但什麼都沒釣到...",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Fishing(bot))

