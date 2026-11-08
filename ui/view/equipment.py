import discord
from discord import ui

from data import SLOTS

from lib.inventory import get_equip_page

class EquipmentView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, page: int = 1):
        super().__init__(timeout = None)
        self.user = user
        self.page = page
        self.render()

    def render(self):
        rows, page, total_page = get_equip_page(self.page, self.user.id)

        self.page = page

        # 創建容器
        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name} 裝備"))
        container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

        for slot_key, item_id in rows:
            print(slot_key, item_id)

            # 解析欄位
            key, _, _ = slot_key.partition(":")
            slot = SLOTS.get(key)

            if slot is None:
                continue

            if item_id is None:
                container.add_item(
                    ui.Section(
                        f"{slot.name}：空", 
                        accessory=ui.Button(label="裝備", style=discord.ButtonStyle.secondary)
                    )
                )
            else:
                container.add_item(
                    ui.Section(
                        f"{slot.name}：{item_id}", 
                        accessory=ui.Button(label="卸下", style=discord.ButtonStyle.secondary)
                    )
                )

        container.add_item(self.page_action(total_page))

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

class EquipButton(ui.Button):
    def __init__(self):
        super().__init__(label = "裝備", style = discord.ButtonStyle.secondary)

    def callback(self, interaction: discord.Interaction):
        pass

class UnequipButton(ui.Button):
    def __init__(self):
        super().__init__(label = "卸下", style = discord.ButtonStyle.secondary)

    def callback(self, interaction: discord.Interaction):
        pass