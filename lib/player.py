from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from cores import logger

from models import Player

if TYPE_CHECKING:
    from data.schema import Item

async def open_item(interaction: discord.Interaction, item: Item, amount: int = 1):
    if not item.is_openable():
        await interaction.response.send_message("這個物品好像無法被打開")
        return

    await interaction.response.send_message("成功打開物品")

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