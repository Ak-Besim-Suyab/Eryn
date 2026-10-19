import discord

from dataclasses import dataclass

"""
本檔案用於定義事件類型
"""

@dataclass
class Event:
    ...

@dataclass
class SelectEvent(Event):
    interaction: discord.Interaction
    value: list
    custom_id: str