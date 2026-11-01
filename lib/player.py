from __future__ import annotations
from typing import TYPE_CHECKING

import discord
from discord import ui
from cores import logger

from models import Player

from lib import item as itemlib
from lib import resource as reslib
from lib.builder import build_container
from lib.view import create_view

import data as registry
from data.schema import ActionType

if TYPE_CHECKING:
    from data.schema import Item, ItemOpen
    from ui import ItemView

async def open_item(view: ItemView, interaction: discord.Interaction, item: Item, times: int = 1):

    if not item.is_openable():
        return False

    open_action: ItemOpen
    open_action = item.get_action(ActionType.OPEN)
    loots = open_action.roll(times)

    descriptions = [f"**成功打開 {times} {item.icon}{item.name}，獲得：**"]

    for (item_id, item_type), quantity in loots.items():
        match item_type:
            case "resource":
                res = registry.resource.get(item_id)
                reslib.give(interaction.user.id, item_id, quantity)
                descriptions.append(f"- {res.icon}{res.name} {quantity}")
            case _:
                pass

    itemlib.remove(interaction.user.id, item.id, times)

    contents = {
        "display_name": interaction.user.display_name,
        "item_icon": item.icon,
        "item_name": item.name,
        "times": times,
        "descriptions": '\n'.join(descriptions)
    }

    view.render()
    await interaction.edit_original_response(view=view)
    await interaction.followup.send(view=create_view("item_opened", **contents))

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