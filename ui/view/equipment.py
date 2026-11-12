import discord
from discord import ui

from data import SLOTS, ITEMS

from lib import inventory, item, player
from models import Inventory

from ui.view import Page

class EquipmentView(Page):
    def __init__(self, user: discord.abc.User):
        super().__init__(user = user, timeout = None)

    def render(self):
        rows, page, total_pages = inventory.get_equip_page(self.page, self.user.id)

        self.page = page
        self.total_pages = total_pages

        # 創建容器
        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name} 裝備"))
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        for slot_key, item_id in rows:

            # 解析欄位
            key, _, _ = slot_key.partition(":")
            slot = SLOTS.get(key)

            if slot is None:
                continue

            if item_id is None:
                container.add_item(
                    ui.Section(
                        f"{slot.name}：空", 
                        accessory=EquipButton(slot.id)
                    )
                )
            else:
                container.add_item(
                    ui.Section(
                        f"{slot.name}：{item_id}", 
                        accessory=ui.Button(label="卸下", style=discord.ButtonStyle.secondary)
                    )
                )

        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
        container.add_item(self.page_action(self.total_pages))

        self.clear_items()
        self.add_item(container)

class EquipButton(ui.Button):
    def __init__(self, slot: str):
        super().__init__(label = "裝備", style = discord.ButtonStyle.secondary)

        self.slot = slot

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=EquipmentChooseView(interaction.user, self.slot))

class UnequipButton(ui.Button):
    def __init__(self):
        super().__init__(label = "卸下", style = discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        pass

class EquipmentChooseView(ui.LayoutView):
    def __init__(
            self,
            user: discord.abc.User,
            slot: str,
            page: int = 1):
        
        super().__init__(timeout = None)

        self.user = user
        self.slot = slot
        self.page = page

        self.render()

    def render(self):

        # 取得符合分類的物品 ID 列表
        item_ids = [i.id for i in ITEMS.find_tags(self.slot)]

        # 取得符合分類的物品
        rows, page, total_pages = inventory.get_page(self.page, self.user.id, item_ids)

        self.page = page

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name} 裝備"))
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        for row in rows:
            if isinstance(row, Inventory):
                line = item.summary_line(row.item_id, row.quantity)
            else:
                line = item.summary_line(row.item_id, 1)

            container.add_item(
                ui.Section(line, accessory=QuickEquipButton(self.user, row.item_id, self.slot))
            )

        container.add_item(self.page_action(total_pages))

        self.clear_items()
        self.add_item(container)

    #NOTE: 翻頁函式之後或許可以提出來做成父類, 然後再讓重用相似函式的子類繼承 (e.g. inventory)
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

class QuickEquipButton(ui.Button):
    def __init__(self,
                 user: discord.abc.User, 
                 item_id: int, 
                 slot: str):
        
        super().__init__(
            label = "快速裝備", 
            style = discord.ButtonStyle.secondary)

        self.user    = user
        self.item_id = item_id
        self.slot    = slot


    async def callback(self, interaction: discord.Interaction):
        success, msg = player.equip(self.user.id, self.item_id, self.slot)

        await interaction.response.send_message(msg)

