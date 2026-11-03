import discord
from discord import ui, SeparatorSpacing

from lib import player
from lib.view import create_view

from data import ITEMS
from data.schema import Item

from models import Inventory

class ItemView(ui.LayoutView):
    def __init__(self, user: discord.abc.User, item_id: str):
        super().__init__(timeout = None)
        self.user = user
        self.item_id = item_id
        self.render()

    def render(self):
        row = Inventory.get_or_none(Inventory.player == self.user.id, Inventory.item_id == self.item_id)

        item = ITEMS.get(self.item_id)

        container = ui.Container()
        container.add_item(ui.TextDisplay(content = f"### {self.user.display_name}"))
        container.add_item(ui.Separator(spacing = SeparatorSpacing.small))

        # 檢查物品是否已為空
        if row is None:
            container.add_item(ui.TextDisplay(content = f"> *你已不再擁有{item.name}。*"))

            self.clear_items()
            self.add_item(container)
            return

        container.add_item(ui.TextDisplay(content = f"{item.icon}{item.name}（你擁有： {row.quantity}）"))
        container.add_item(ui.ActionRow(UseSelect(item, row.quantity)))

        self.clear_items()
        self.add_item(container)

class UseSelect(ui.Select):
    """ 這個選單用於對物品使用什麼動作
    """
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

        actions = [
            ("food", (f"吃", "eat")),
            ("loot", (f"打開", "open")),
            ("loot", (f"打開全部", "open_all"))
        ]

        # NOTE: 如果我這裡都已經篩選過何種動作有使用結果，那我還需要在後面的邏輯再判定一次嗎？
        options = [discord.SelectOption(label = label, value = value) for flag, (label, value) in actions if item.has_component(flag)]
        
        super().__init__(
            placeholder = "要對這個物品做什麼？",
            options = options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        match self.values[0]:
            case "consume":
                pass
            case "open":

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

            case "open_all":
                pass