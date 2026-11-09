""" 
此類別用於建構背包 UI
self.category 用於保存當前顯示的物品類別, 在分類表單中使用
self.rows 用於保存抽取的背包結果, 在選擇表單中使用
"""
import discord
from discord import ui, SeparatorSpacing

from data import ITEMS
from models import Inventory, ItemInstance

from ui.view.item import ItemView

from lib.inventory import get_page
from lib.item import summary_line, sort_key

class InventoryView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, page: int = 1, category: str = "all"):
        super().__init__(timeout = None)
        self.user = user
        self.page = page
        self.category = category
        self.render()

    def render(self):
        # 取得當前頁面的物品列表
        rows, page, total_pages = get_page(self.page, self.user.id, self.get_item_ids())

        # 存入物件狀態, 並進行排序
        self.page = page
        rows.sort(key=sort_key)

        # 將物品轉換為字串, 並根據物品分類修正參數
        # NOTE: 這段好像可以刪除？
        lines = []
        for row in rows:
            if isinstance(row, Inventory):
                lines.append((row.id, summary_line(row.item_id, row.quantity)))
            else:
                lines.append(summary_line(row.item_id, 1))
        
        if not lines: lines = ["> *沒有任何可以顯示的物品。*"]

        # 創建容器
        container = ui.Container(accent_color = 0)
        container.add_item(ui.TextDisplay(content = f"## 🪎 {self.user.display_name} 背包"))
        container.add_item(ui.Separator(spacing=SeparatorSpacing.large))

        # 印出物品列表
        for row in rows:
            if isinstance(row, Inventory):
                line = summary_line(row.item_id, row.quantity)
            else:
                line = summary_line(row.item_id, 1)

            container.add_item(
                ui.Section(line, accessory=ItemButton(row))
            )

        container.add_item(self.category_action())
        container.add_item(self.page_action(total_pages))

        # 清除舊元件，加入更新後的元件
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
            "all"      : "全部",
            "loot"     : "戰利品",
            "equipment": "裝備",
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
            case "all": 
                return None
            case _: 
                tags = self.category.split(":")
                return [item.id for item in ITEMS.find_tags(*tags)]

class ItemButton(ui.Button):

    def __init__(self, record: Inventory | ItemInstance):
        self.record = record

        super().__init__(
            label = "選擇",
            style = discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=ItemView(interaction.user, self.record)) 