import discord

from engines.fishing_engine import FishingEngine
from context import Context


class FishingAgainButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="再釣一次", style=discord.ButtonStyle.primary)
        self.engine = FishingEngine()

    async def callback(self, interaction: discord.Interaction):
        payload = self.engine.cast(interaction)

        new_view = type(self.view)()

        if not payload:
            embed = discord.Embed(
                title=interaction.user.display_name,
                description="你在附近的水域垂釣，但什麼都沒釣到...",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, view=new_view)
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
            title=interaction.user.display_name,
            description="你在附近的水域垂釣，好像有魚上鉤...",
            color=discord.Color.blue()
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

        await interaction.response.send_message(embed=embed, view=new_view)