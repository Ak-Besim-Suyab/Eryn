import discord

from system import registry
from game import model
from game import ui

class Context:
    """
    該類別為負責連結連續指令與元件的上下文容器，命名來源於 discord.py 傳統文字指令傳入的參數。

    .. `message_id`: 訊息提取
    .. `page`: 連續對話的文本頁數，用於控制文本輸出的順序。
    """
    def __init__(self, message_name: str):
        self.message_name = message_name
        self.messages = registry.message.get(message_name)
        self.page = 1

    async def send(self, interaction: discord.Interaction):
        """
        最主要的訊息輸出函式。
        """
        page = self.messages.get_page(self.page)
        if page is None:
            await interaction.response.send_message("對話文本似乎有誤，已結束對話，請聯絡管理員檢查。", ephemeral=True)
            return

        embeds = await self._create_embeds(page.embeds) if page.embeds else []
        
        view = ui.View(page.view, self)

        await interaction.response.send_message(embeds=embeds, view=view, ephemeral=page.ephemeral)

    async def _create_embeds(self, embeds: list[model.Embed]):
        """將訊息元件中的 Embed 轉換為 ui.Embed"""
        _embeds = []
        for embed in embeds:
            _embed = ui.Embed(embed)
            _embeds.append(_embed)
        return _embeds