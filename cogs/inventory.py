"""
背包功能模組，包含 /背包 指令、InventoryView 視圖與物品按鈕元件。
"""
import discord
from discord import app_commands, ui
from discord.ext import commands

from data import ITEMS
from lib.inventory import get_page
from lib.item import summary_line
from models import Inventory, ItemInstance
from ui.view import Page
from ui.view.item import ItemView


class InventoryCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="背包", description="查看背包")
    async def inventory(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=InventoryView(interaction.user))


class InventoryView(Page):
    def __init__(self, user: discord.abc.User, tags: list[str] | None = None):
        self.tags = tags

        super().__init__(user=user, timeout=None)

    def render(self):
        # 取得當前頁面的物品列表
        rows, page, total_pages = get_page(self.page, self.user.id, self.get_item_ids())

        # 存入物件狀態
        self.page = page
        self.total_pages = total_pages

        # 建立容器
        container = ui.Container(accent_color=0)
        container.add_item(ui.TextDisplay(content=f"## 🪎 {self.user.display_name} 背包"))

        # 印出物品列表
        if not rows:
            container.add_item(ui.TextDisplay(content="> *沒有任何可以顯示的物品。*"))
        else:
            for row in rows:
                quantity = row.quantity if isinstance(row, Inventory) else 1
                line = summary_line(row.item_id, quantity)
                container.add_item(ui.Section(line, accessory=ItemButton(row)))

        container.add_item(self.category_action())
        container.add_item(self.page_action(self.total_pages))

        # 清除舊元件，加入更新後的元件
        self.clear_items()
        self.add_item(container)

    def category_action(self):
        tags = {
            "all"      : "全部（忽略所有分類）",
            "equipment": "裝備",
            "food"     : "食物",
            "loot"     : "戰利品",
        }

        options = [
            discord.SelectOption(label=value, value=key)
            for key, value in tags.items()
        ]

        select = ui.Select(
            placeholder="選擇分類篩選物品",
            min_values=0,
            max_values=len(tags),
            options=options,
        )
        select.callback = self.on_category

        return ui.ActionRow(select)

    async def on_category(self, interaction: discord.Interaction):
        values = interaction.data["values"]
        self.tags = values if "all" not in values else None
        self.page = 1
        self.render()
        await interaction.response.edit_message(view=self)

    def get_item_ids(self) -> list[str] | None:
        if self.tags is None:
            return None
        return [item.id for item in ITEMS.find_tags(*self.tags, match_any=True)]


class ItemButton(ui.Button):
    def __init__(self, record: Inventory | ItemInstance):
        self.record = record

        super().__init__(
            label="選擇",
            style=discord.ButtonStyle.secondary,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=ItemView(interaction.user, self.record))


async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryCog(bot))
