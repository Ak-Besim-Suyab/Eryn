"""
該模組用於匯總戰利品發放邏輯，根據不同的戰利品類型套用對應的邏輯
"""
from collections import Counter
from typing import Iterable

from cores import database
from data import LOOT_TABLES
from lib import item
from lib import material
from lib import currency
from lib import player

def give(player_id: int, item_type: str, reward: str, quantity: int):

    if quantity < 0:
        return
    
    match item_type:
        case "item": item.give(player_id, reward, quantity)
        case "material" | "resource": material.give(player_id, reward, quantity)
        case "currency": currency.give(player_id, reward, quantity)
        case _: raise ValueError(f"unknown item type: {item_type}")

def roll_region(player_id: int, times: int = 1) -> Counter | None:
    """
    依據玩家目前所在地區抽取戰利品表，若該地區沒有戰利品表則返回 None
    """
    loot_table = LOOT_TABLES.get(player.get_region(player_id))
    if not loot_table:
        return None
    return loot_table.roll(times)

def give_region_reward(player_id: int, times: int = 1) -> Counter | None:
    """
    依據玩家目前所在地區抽取並發放相應戰利品，返回本次抽取結果（無戰利品表則返回 None）
    """
    rolled = roll_region(player_id, times)
    if not rolled:
        return None

    with database.atomic():
        for (item_type, item_id), quantity in rolled.items():
            give(player_id, item_type, item_id, quantity)

    return rolled

def give_region_rewards(player_ids: Iterable[int], times: int = 1):
    """
    批次依據多位玩家所在地區抽取並在單一交易中發放戰利品
    """
    rewards: list[tuple[int, Counter]] = []
    for player_id in player_ids:
        rolled = roll_region(player_id, times)
        if rolled:
            rewards.append((player_id, rolled))

    if not rewards:
        return

    with database.atomic():
        for player_id, rolled in rewards:
            for (item_type, item_id), quantity in rolled.items():
                give(player_id, item_type, item_id, quantity)