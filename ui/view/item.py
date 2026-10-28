import discord
from discord import ui, SeparatorSpacing

import data
from data.schema import Item

from lib import item

class ItemView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, item_id: str, quantity: int = 1):
        super().__init__(timeout = None)
        self.user = user
        self.item_id = item_id
        self.quantity = quantity

        self.render()

    def render(self):
        item = data.item.get(self.item_id)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"### {self.user.display_name}"))
        container.add_item(ui.Separator(spacing = SeparatorSpacing.small))
        container.add_item(ui.TextDisplay(content = f"{item.emoji}{item.name}（你擁有： {self.quantity}）"))
        container.add_item(ui.ActionRow(UseSelect(item)))

        self.add_item(container)

class UseSelect(ui.Select):
    """ 這個選單用於對物品使用什麼動作
    """
    def __init__(self, item: Item):
        self.item = item

        actions = {
            "consumable": ("使用物品", "consume"),
            "openable":   ("打開物品", "open"),
        }

        options = [discord.SelectOption(label = label, value = value) for flag, (label, value) in actions.items() if getattr(self.item.flags, flag)]
        
        super().__init__(
            placeholder = "要對這個物品做什麼？",
            options = options
        )

    async def callback(self, interaction: discord.Interaction):
        match self.values[0]:
            case "consume":
                # item.consume(interaction.user)
                print("consumed.")
            case "open":
                # item.open(interaction, self.item)
                # 目前選擇邏輯直到這裡已實作完成，但後續邏輯仍需要琢磨如何規劃與實現
                print("opened.")