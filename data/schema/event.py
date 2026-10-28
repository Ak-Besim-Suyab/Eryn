"""
    這裡用於定義事件類型

    父類別: Event

        :: id: str

          - 事件的唯一識別碼, 宣告時需要傳入唯一的識別碼, 相同類型的事件可能有非常多不同的分派, 為適配 Event 的泛用性而設置此參數
          - 例如: SelectEvent 用於以資料驅動所生產的下拉式選單觸發的 on_interaction 監聽, 這類選單無法自訂 callback 函式, 須透過能傳遞的參數來實現

    子類別: SelectEvent

        :: interaction: discord.Interaction
        :: value: list
        :: custom_id: str

          - 由於 SelectEvent 可能乘載不同分類的事件, 使用時可以將 custom_id 傳入 Event.id 作為唯一識別
"""
import discord
from dataclasses import dataclass

@dataclass
class Event:
    id: str

@dataclass
class ButtonEvent(Event):
    interaction: discord.Interaction
    custom_id: str

@dataclass
class SelectEvent(Event):
    interaction: discord.Interaction
    values: list
    custom_id: str