import discord

from engines.fishing_engine import FishingEngine
from ui.views.fishing_view import FishingView

from context import Context

class FishingSession:
    def __init__(self):
        self.engine = FishingEngine()
        self.view = FishingView(self)
    
    async def start(self, interaction: discord.Interaction):
        payload = self.engine.cast(interaction)

        if not payload:
            await self._broadcast_fish_missed(interaction)
        else:
            await self._broadcast_fish_successed(interaction, payload)


    async def _broadcast_fish_missed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=interaction.user.display_name, 
            description="你在附近的水域垂釣，但什麼都沒釣到...", 
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=self.view)
    
    async def _broadcast_fish_successed(self, interaction: discord.Interaction, payload):
        item_manager = Context.get_manager("item")
        lines = []

        for item in payload:
            if "item_id" in item:
                item_obj = item_manager.get_item(item["item_id"])
                item_name = item_obj.name if item_obj else item["item_id"]
                lines.append(f"**{item_name}**× {item['quantity']}")

        embed = discord.Embed(
            title = interaction.user.display_name, 
            description = "你在附近的水域垂釣，好像有魚上鉤...", 
            color=discord.Color.blue()
        )

        embed.add_field(
            name="你獲得：", 
            value="\n".join(lines), 
            inline=False
        )

        for item in payload:
            if item.get("event_type") == "treasure":
                currency = item.get("currency", 0)
                embed.add_field(
                    name="你在水域附近發現寶藏！",
                    value=f"獲得額外 {currency} 金幣",
                    inline=False
                )
                
        await interaction.response.send_message(embed=embed, view=self.view)