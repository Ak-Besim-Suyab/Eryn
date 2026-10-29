import discord
from discord import ui, SeparatorSpacing

from lib import player

import data
from data.schema import Item

from models import Inventory

class ItemView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, item_id: str):
        super().__init__(timeout = None)
        self.user = user
        self.item_id = item_id
        self.render()

    def render(self):
        row: Inventory
        row = Inventory.get_or_none(Inventory.player == self.user.id, Inventory.item_id == self.item_id)
        quantity = row.quantity

        item = data.item.get(self.item_id)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"### {self.user.display_name}"))
        container.add_item(ui.Separator(spacing = SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(content = f"{item.emoji}{item.name}（你擁有： {quantity}）"))
        container.add_item(ui.ActionRow(UseSelect(item, quantity)))

        self.clear_items()
        self.add_item(container)

class UseSelect(ui.Select):
    """ 這個選單用於對物品使用什麼動作
    """
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

        actions = [
            ("consumable", (f"使用物品", "consume")),
            ("openable",   (f"打開物品", "open")),
            ("openable",   (f"打開物品 ({quantity})", "open_all"))
        ]

        # NOTE: 如果我這裡都已經篩選過何種動作有使用結果，那我還需要在後面的邏輯再判定一次嗎？
        options = [discord.SelectOption(label = label, value = value) for flag, (label, value) in actions if getattr(self.item.flags, flag)]
        
        super().__init__(
            placeholder = "要對這個物品做什麼？",
            options = options
        )

    async def callback(self, interaction: discord.Interaction):
        match self.values[0]:
            case "consume":
                pass
            case "open":
                # 目前選擇邏輯直到這裡已實作完成，但後續邏輯仍需要琢磨如何規劃與實現
                await player.open_item(self.view, interaction, self.item, 1)
            case "open_all":
                await player.open_item(self.view, interaction, self.item, self.quantity)