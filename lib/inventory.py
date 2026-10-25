"""此函式庫用於建構背包相關函式
"""
import math
import discord
from discord import ui

import data
from cores import logger
from models import Player, Inventory
from lib import builder

MAX_ROW = 20

# 此函式用於取得背包頁數, 與控制頁面修正
def get_page(player_id: int, page: int) -> list[str]:
    """取得背包清單
    """
    rows = (Inventory
            .select()
            .where((Inventory.player == player_id) & (Inventory.quantity > 0))
            .order_by(Inventory.item_id))

    total_pages = max(1, math.ceil(rows.count() / MAX_ROW))
    page = min(max(page, 1), total_pages)

    return list(rows.paginate(page, MAX_ROW)), page, total_pages

# 此函式用於格式化物品文本
def format_row(row: Inventory) -> str:
    item = data.item.get(row.item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {row.item_id}")
        return f"- ❓{row.item_id} - {row.quantity}"
    
    return f"- {item.emoji}{item.name} - {row.quantity} "
    
class InventoryView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, page: int = 1):
        super().__init__(timeout = None)
        self.user = user
        self.page = page
        self.render()

    def render(self):
        Player.get_or_create(id=self.user.id)
        rows, self.page, total_pages = get_page(self.user.id, self.page)

        lines = [format_row(r) for r in rows] or ["> *背包裡什麼都沒有。*"]

        container = builder.build_container(
            data.container.get("inventory"),
            player_name = self.user.display_name,
            items = "\n".join(lines),
            page = self.page,
            total_pages = total_pages,
        )

        prev_btn = ui.Button(label="上一頁", style=discord.ButtonStyle.secondary,
                             disabled=self.page <= 1)
        next_btn = ui.Button(label="下一頁", style=discord.ButtonStyle.secondary,
                             disabled=self.page >= total_pages)
        prev_btn.callback = self.on_prev
        next_btn.callback = self.on_next

        container.add_item(ui.ActionRow(prev_btn, next_btn))

        self.clear_items()
        self.add_item(container)

    async def on_prev(self, interaction: discord.Interaction):
        self.page -= 1
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_next(self, interaction: discord.Interaction):
        self.page += 1
        self.render()
        await interaction.response.edit_message(view=self)