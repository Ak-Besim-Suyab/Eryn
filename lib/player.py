from __future__ import annotations
from typing import TYPE_CHECKING

import discord
from discord import ui
from cores import logger

from models import Player

from lib import item as itemlib
from lib import resource as reslib
from lib.builder import build_container

import data
from data.schema import ActionType

if TYPE_CHECKING:
    from data.schema import Item, ItemOpen
    from ui import ItemView

async def open_item(view: ItemView, interaction: discord.Interaction, item: Item, times: int = 1):

    if not item.is_openable():
        await interaction.response.send_message("這個物品好像無法被打開")
        return

    await interaction.response.defer(ephemeral=True)

    open_action: ItemOpen
    open_action = item.get_action(ActionType.OPEN)
    loots = open_action.roll(times)

    reward_lines = []
    for (item_id, item_type), quantity in loots.items():

        match item_type:
            case "resource":
                reslib.give(interaction.user.id, item_id, quantity)
                reward_lines.append(f"{quantity} 個 {item_id}")
            case "item":
                # reward = data.item.get(item_id)
                # itemlib.give(interaction.user, reward.id, quantity)
                # reward_lines.append(f"{quantity} 個 {reward.name}")
                pass

    itemlib.remove(interaction.user.id, item.id, quantity)

    logger.debug(f"成功運行物品開啟")

    message = f"成功打開 {times} 個物品，獲得: "+ ', '.join(reward_lines)

    kwargs = {
        "display_name": interaction.user.display_name,
        "item_emoji": item.emoji,
        "item_name": item.name,
    }

    #NOTE 是不是可以做一個 builder_view(*args) 透過 *args 展開參數，這樣好像可以實現多容器 view
    container = build_container(data.container.get("item_opened"))

    view.render()
    await interaction.edit_original_response(view=view)
    await interaction.followup.send(view=ui.LayoutView().add_item(container))

def get_timestamp_daily(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_daily

def set_timestamp_daily(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_daily = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的每日時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的每日時間戳記")

def get_timestamp_voice(player_id: int):
    player: Player
    player, _ = Player.get_or_create(id=player_id)
    return player.timestamp_voice

def set_timestamp_voice(player_id: int, timestamp: float = None):
    Player.get_or_create(id=player_id)
    (Player
    .update(timestamp_voice = timestamp)
    .where(Player.id == player_id)
    .execute())

    if timestamp is None:
        logger.debug(f"成功移除 {player_id} 的語音時間戳記")
    else:
        logger.debug(f"成功保存 {player_id} 的語音時間戳記")