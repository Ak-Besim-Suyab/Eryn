"""
該模組用於匯總戰利品發放邏輯，根據不同的戰利品類型套用對應的邏輯
"""

from lib import item
from lib import resource
from lib import currency

def give(player_id: int, item_type: str, reward: str, quantity: int):

    if quantity < 0:
        return
    
    match item_type:
        case "item": item.give(player_id, reward, quantity)
        case "resource": resource.give(player_id, reward, quantity)
        case "currency": currency.give(player_id, reward, quantity)
        case _: raise ValueError(f"unknown item type: {item_type}")