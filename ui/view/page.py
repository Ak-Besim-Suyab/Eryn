from abc import ABC, abstractmethod

import discord
from discord import ui

class Page(ABC, ui.LayoutView):
    """
    物品欄介面父類
    
    該類別實作通用翻頁與更新按鈕並提供子類自由加入在容器或視圖的元件裡, 子類別需要實作 render 方法以配合按鈕刷新介面
    任何需要翻頁功能的介面都可以繼承此類別
    """
    def __init__(self, user: discord.abc.User, timeout: float | None = 180):
        super().__init__(timeout = timeout)

        self.user        = user
        self.page        = 1
        self.total_pages = 1
        self.render()

    @abstractmethod
    def render(self): ...

    def page_action(self, total_pages: int):
        #NOTE: 之後看能不能把文字改成自訂圖案
        home_btn = ui.Button(label = "首頁", style = discord.ButtonStyle.secondary, disabled = self.page == 1)
        prev_btn = ui.Button(label = "前頁", style = discord.ButtonStyle.secondary, disabled = self.page <= 1)

        refresh_btn = ui.Button(label = "更新", style = discord.ButtonStyle.secondary)

        next_btn = ui.Button(label = "後頁", style = discord.ButtonStyle.secondary, disabled = self.page >= total_pages)
        last_btn = ui.Button(label = "末頁", style = discord.ButtonStyle.secondary, disabled = self.page == total_pages)

        home_btn.callback = self.on_home
        prev_btn.callback = self.on_prev

        refresh_btn.callback = self.on_refresh

        next_btn.callback = self.on_next
        last_btn.callback = self.on_last

        return ui.ActionRow(home_btn, prev_btn, refresh_btn, next_btn, last_btn)

    async def on_home(self, interaction: discord.Interaction):
        self.page = 1
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_prev(self, interaction: discord.Interaction):
        self.page -= 1
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_refresh(self, interaction: discord.Interaction):
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_next(self, interaction: discord.Interaction):
        self.page += 1
        self.render()
        await interaction.response.edit_message(view=self)

    async def on_last(self, interaction: discord.Interaction):
        self.page = self.total_pages
        self.render()
        await interaction.response.edit_message(view=self)