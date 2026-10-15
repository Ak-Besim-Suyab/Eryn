import discord
from discord import ui, SeparatorSpacing

from typing import Self

"""
    此類別用於建造 Discord 視圖中的容器 (Container) 元件, 以建造者模式構築
"""

class ContainerBuilder:
    def __init__(self, accent_color: discord.Color):
        self.accent_color = accent_color
        self.items = []

    def text(self, content: str) -> Self:
        self.items.append(lambda: ui.TextDisplay(content=content))
        return self

    def seperator(self, space: SeparatorSpacing = SeparatorSpacing.large) -> Self:
        self.items.append(lambda: ui.Separator(spacing=space))
        return self

    def build(self) -> ui.Container:
        container = ui.Container()
        for item in self.items:
            container.add_item(item())
        return container