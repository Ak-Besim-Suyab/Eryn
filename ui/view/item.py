import discord
from discord import ui, SeparatorSpacing

from lib import player
from lib.view import create_view
from lib.item import summary_line

from data import ITEMS
from data.schema import Item

from model import Inventory, ItemInstance

class ItemView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, row: Inventory | ItemInstance):
        super().__init__(timeout = None)
        self.user = user
        self.row = row
        self.render()

    def render(self):
        # 重新獲取物品 (裝備或背包, 可擴充分類)
        item = ITEMS.get(self.row.item_id)
        if item.is_equippable():
            row = ItemInstance.get_or_none(
                ItemInstance.player == self.user.id,
                ItemInstance.id == self.row.id,
                ItemInstance.item_id == self.row.item_id)

            if row is None:
                quantity = 0
            else:
                quantity = 1
        else:
            row = Inventory.get_or_none(
                Inventory.player == self.user.id,
                Inventory.id == self.row.id,
                Inventory.item_id == self.row.item_id)

            if row is None:
                quantity = 0
            else:
                quantity = row.quantity

        # 建構容器
        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"## {self.user.display_name} 物品"))
        container.add_item(ui.Separator(spacing=SeparatorSpacing.large))

        # 檢查物品是否已為空
        if row is None:
            container.add_item(ui.TextDisplay(content = f"> *你已不再擁有{item.name}。*"))

            self.clear_items()
            self.add_item(container)
            return

        container.add_item(ui.TextDisplay(content=summary_line(item.id, quantity)))
        container.add_item(ui.ActionRow(UseSelect(item, quantity)))

        self.clear_items()
        self.add_item(container)

class UseSelect(ui.Select):
    """ 這個選單用於對物品使用什麼動作
    """
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

        # 蒐集物品可執行行動
        placeholder = "要對這個物品做什麼？"
        disabled = False

        actions = []
        if item.is_equippable():
            actions.append(("裝備", "equip"))

        if item.is_lootable():
            actions.append(("打開", "loot"))

        if item.is_consumable():
            actions.append(("使用", "consume"))

        # 印出行動
        options = []
        for label, value in actions:
            options.append(discord.SelectOption(label = label, value = value))

        # 若沒有任何行動, 印出空行動, 避免空選項報錯
        if not options:
            placeholder = "沒有可用行動"
            disabled = True
            
            options = [discord.SelectOption(label = "沒有可用行動", value = 0)]
        
        super().__init__(
            placeholder = placeholder,
            min_values = 1,
            max_values = 1,
            options = options,
            disabled = disabled
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        match self.values[0]:
            case "equip":
                pass
            case "loot":
                contents = {
                    "display_name": interaction.user.display_name,
                    "item_name": self.item.name,
                }

                success, item_lines = player.open_item(interaction.user.id, self.item, 1)

                if not success:
                    await interaction.followup.send(view=create_view("open_fail", **contents))
                    return

                descriptions = [f"**獲得物品：**"]
                descriptions.extend(item_lines)

                contents.update({"descriptions": "\n".join(descriptions)})

                view = self.view
                view.render()

                await interaction.edit_original_response(view=view)
                await interaction.followup.send(view=create_view("open_success", **contents))

            case _:
                await interaction.followup.send(f"> *你拿起{self.item.name}，但似乎什麼事也不能做。*")