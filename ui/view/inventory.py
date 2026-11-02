""" 此類別用於建構背包 UI
    self.category 用於保存當前顯示的物品類別, 在分類表單中使用
    self.rows 用於保存抽取的背包結果, 在選擇表單中使用
"""
import discord
from discord import ui

import data
from cores import logger
from models import Inventory

from .item import ItemView

from lib.inventory import get_page
from lib.item import summary_line

class InventoryView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, page: int = 1, category: str = "all"):
        super().__init__(timeout = None)
        self.user = user
        self.page = page
        self.category = category
        self.rows = []
        self.render()

    def render(self):
        rows, self.page, total_pages = get_page(self.user.id, self.page, self.get_item_ids())
        
        self.rows = rows

        lines = [summary_line(row.item_id, row.quantity) for row in rows] or ["> *沒有任何可以顯示的物品。*"]

        container = ui.Container(accent_color = 0)
        container.add_item(ui.TextDisplay(content = f"### {self.user.display_name}"))
        container.add_item(ui.TextDisplay(content = "\n".join(lines)))
        container.add_item(self.category_action())

        # 檢查物品是否合法，若為空或僅有不合法物品，不顯示表單
        valid_rows = [row for row in rows if data.ITEMS.get(row.item_id) is not None]
        if valid_rows:
            container.add_item(ui.ActionRow(ItemSelect(valid_rows)))
            
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

    def category_action(self):

        categorys = {
            "all":        "全部",
            "openable":   "可使用",
            "comsumable": "可消耗",
        }

        options = []
        for key, value in categorys.items():
            options.append(discord.SelectOption(label = value, value = key))

        select = ui.Select(
            placeholder = "選擇物品分類",
            options = options
        )
        select.callback = self.on_category

        return ui.ActionRow(select)

    async def on_category(self, interaction: discord.Interaction):
        self.category = interaction.data["values"][0]
        self.page = 1
        self.render()
        await interaction.response.edit_message(view=self)

    def get_item_ids(self) -> list[str]:
        match self.category:
            case "all": return None
            case "openable": return [item.id for item in data.ITEMS.find_flag(openable=True)]

class ItemSelect(ui.Select):
    """ 這個表單用來讀取並列出玩家指定分類的物品, 表單選項受到傳入的串列影響, 串列則由上層來自 Inventory 的讀取函式取得
    """
    def __init__(self, rows: list[Inventory]):
        self.rows = rows

        options = []
        for row in rows:
            item = data.ITEMS.get(row.item_id)
            if item is None:
                continue

            options.append(discord.SelectOption(label = item.name, value = item.id))
        
        super().__init__(
            placeholder = "選擇物品",
            options = options
        )

    # 這裡使用 send_message 回覆新視窗，以便於重複對不同物品進行操作
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=ItemView(interaction.user, self.values[0])) 