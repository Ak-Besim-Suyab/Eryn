import discord

from system.registry import Item ,item_registry

from system.models import Player
from system.models import Inventory

from game.dialogues import DialogueView

async def purchase(interaction: discord.Interaction, selected_options: dict[str, list[str]]):
    """
    `custom_id`: 傳入選項的行為, 傳入後會拆解成 `行為:行為目標`
    `values`: 傳入選擇的值
    """
    items: list[Item] = []

    for custom_id, values in selected_options.items(): 
        match custom_id:
            case "purchase:item":
                # 該匹配為購買物品, 傳入的串列應為物品列表
                for value in values:
                    item = item_registry.get(value)
                    if item:
                        items.append(item)
            case "purchase:quantity":
                quantity = int(values[0])

    player: Player = Player.get_or_create_player(interaction.user.id)

    # 計算加總
    total_unit_price = sum(item.price for item in items)
    cost = total_unit_price * quantity
    if player.currency < cost:
        await interaction.response.send_message("❌ 你沒有足夠的金幣購買這些物品。", ephemeral=True)
        return

    # 運行玩家邏輯
    player.currency -= cost
    for item in items:
        Inventory.add_item(interaction.user.id, item.id, quantity)

    item_descriptions = [item.to_description(type="reward", quantity=quantity) for item in items]

    await DialogueView(dialog_name="purchase_success").send(interaction=interaction, payloads={"item_descriptions": item_descriptions})