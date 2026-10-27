"""此函式庫用於建構背包相關函式
"""
import math
import discord
from discord import ui

import data
from cores import logger
from models import Player, Inventory
from lib import builder

from ui.utils import LARGE_SEPARATOR

MAX_ROW = 20

def get_page(player_id: int, page: int, item_ids: list[str] = None) -> tuple[list[str], int, int]:
    """ 取得物品列表並計算要列出的頁數

        - page: 要列出的頁數, 這裡由外部傳入, 物件有預設值 1
        - item_ids: 指定的物品 ID 列表, 未指定 (None) 時將列出所有物品
    """
    Player.get_or_create(id = player_id)

    rows = (Inventory
            .select()
            .where(Inventory.player == player_id)
            .where(Inventory.quantity > 0))

    if item_ids is not None:
        rows = rows.where(Inventory.item_id.in_(item_ids))

    rows = rows.order_by(Inventory.item_id)

    total_pages = max(1, math.ceil(rows.count() / MAX_ROW))
    page = min(max(page, 1), total_pages)

    return list(rows.paginate(page, MAX_ROW)), page, total_pages


def format_row(row: Inventory) -> str:
    item = data.item.get(row.item_id)
    if item is None:
        logger.warning(f"背包內存在未定義的道具: {row.item_id}")
        return f"- ❓{row.item_id} - {row.quantity}"
    
    return f"- {item.emoji}{item.name} - {row.quantity} "


class InventoryView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, page: int = 1, category: str = "all"):
        super().__init__(timeout = None)
        self.user = user
        self.page = page
        self.category = category
        self.render()

    def render(self):
        rows, self.page, total_pages = get_page(self.user.id, self.page, self.get_item_ids())

        lines = [format_row(r) for r in rows] or ["> *背包裡什麼都沒有。*"]

        container = ui.Container(accent_color = 0)
        container.add_item(ui.TextDisplay(content = "\n".join(lines)))
        container.add_item(self.page_action(total_pages))

        self.clear_items()
        self.add_item(container)

    def page_action(self, total_pages):
        prev_btn = ui.Button(label = "上一頁", style = discord.ButtonStyle.secondary, disabled = self.page <= 1)
        next_btn = ui.Button(label = "下一頁", style = discord.ButtonStyle.secondary, disabled = self.page >= total_pages)
        prev_btn.callback = self.on_prev
        next_btn.callback = self.on_next

        return ui.ActionRow(prev_btn, next_btn)

    async def on_prev(self, interaction: discord.Interaction):
        self.page -= 1
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_next(self, interaction: discord.Interaction):
        self.page += 1
        self.render()
        await interaction.response.edit_message(view=self)

    def get_item_ids(self) -> list[str]:
        match self.category:
            case "all": return None
            case "openable": return [item.id for item in data.item.find_flag(openable=True)]