import discord

from engines.fishing_engine import FishingEngine
from ui.views.fishing_view import FishingView

from context import Context

class FishingSession:
    def __init__(self, interaction):
        self.interaction = interaction
        self.engine = FishingEngine()
        self.view = FishingView(self)
    
    async def start(self):
        payload = self.engine.cast(self.interaction)

        view = FishingView(self)

        if not payload:
            embed = discord.Embed(
                title=self.interaction.user.display_name,
                description="你在附近的水域垂釣，但什麼都沒釣到...",
                color=discord.Color.blue()
            )
            await self.interaction.response.send_message(embed=embed, view=view)
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
            title = self.interaction.user.display_name, 
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
 
        await self.interaction.response.send_message(embed=embed, view=view)