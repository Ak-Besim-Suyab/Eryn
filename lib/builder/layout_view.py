from discord import ui

from .container import ContainerBuilder

"""
    此類別用於建造 Discord 視圖, 以建造者模式構築

    由於單個 LayoutView 不僅能包含複數 Container 元件, 亦可包含其他 Item 元件, 因此也將適用於建造者模式
    目前僅實作包含 ContainerBuilder 所生產的 Container 元件
"""

class LayoutViewBuilder:
    def __init__(self, timeout = None):
        self.timeout = timeout
        self.containers: list[ContainerBuilder] = []

    def build(self) -> ui.LayoutView:
        view = ui.LayoutView(timeout = self.timeout)
        for container_builder in self.containers:
            view.add_item(container_builder.build())
        return view